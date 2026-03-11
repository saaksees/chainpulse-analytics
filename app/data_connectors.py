#!/usr/bin/env python3
"""
Real-time Data Connectors
Connect to various data sources for live data integration
"""

import pandas as pd
import sqlite3
import json
import requests
from datetime import datetime, timedelta
import os
from typing import Dict, List, Optional, Any
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataConnector:
    """Base class for all data connectors"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.connection = None
        
    def connect(self) -> bool:
        """Establish connection to data source"""
        raise NotImplementedError
        
    def disconnect(self):
        """Close connection to data source"""
        if self.connection:
            self.connection.close()
            
    def test_connection(self) -> Dict[str, Any]:
        """Test if connection is working"""
        try:
            success = self.connect()
            return {
                'success': success,
                'message': 'Connection successful' if success else 'Connection failed',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Connection error: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
        finally:
            self.disconnect()
            
    def fetch_data(self, query: str = None, **kwargs) -> pd.DataFrame:
        """Fetch data from source"""
        raise NotImplementedError

class SQLiteConnector(DataConnector):
    """SQLite database connector"""
    
    def connect(self) -> bool:
        try:
            db_path = self.config.get('database_path', 'chainpulse.db')
            self.connection = sqlite3.connect(db_path)
            return True
        except Exception as e:
            logger.error(f"SQLite connection failed: {e}")
            return False
            
    def fetch_data(self, query: str = None, **kwargs) -> pd.DataFrame:
        if not self.connection:
            self.connect()
            
        if not query:
            # Default query to get order data
            query = """
            SELECT * FROM orders 
            WHERE created_at >= date('now', '-30 days')
            ORDER BY created_at DESC
            """
            
        try:
            df = pd.read_sql_query(query, self.connection)
            logger.info(f"Fetched {len(df)} records from SQLite")
            return df
        except Exception as e:
            logger.error(f"SQLite query failed: {e}")
            return pd.DataFrame()

class PostgreSQLConnector(DataConnector):
    """PostgreSQL database connector"""
    
    def connect(self) -> bool:
        try:
            import psycopg2
            conn_params = {
                'host': self.config.get('host', 'localhost'),
                'port': self.config.get('port', 5432),
                'database': self.config.get('database'),
                'user': self.config.get('username'),
                'password': self.config.get('password')
            }
            self.connection = psycopg2.connect(**conn_params)
            return True
        except ImportError:
            logger.error("psycopg2 not installed. Run: pip install psycopg2-binary")
            return False
        except Exception as e:
            logger.error(f"PostgreSQL connection failed: {e}")
            return False
            
    def fetch_data(self, query: str = None, **kwargs) -> pd.DataFrame:
        if not self.connection:
            self.connect()
            
        if not query:
            query = """
            SELECT * FROM orders 
            WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
            ORDER BY created_at DESC
            """
            
        try:
            df = pd.read_sql_query(query, self.connection)
            logger.info(f"Fetched {len(df)} records from PostgreSQL")
            return df
        except Exception as e:
            logger.error(f"PostgreSQL query failed: {e}")
            return pd.DataFrame()

class MySQLConnector(DataConnector):
    """MySQL database connector"""
    
    def connect(self) -> bool:
        try:
            import pymysql
            conn_params = {
                'host': self.config.get('host', 'localhost'),
                'port': self.config.get('port', 3306),
                'database': self.config.get('database'),
                'user': self.config.get('username'),
                'password': self.config.get('password'),
                'charset': 'utf8mb4'
            }
            self.connection = pymysql.connect(**conn_params)
            return True
        except ImportError:
            logger.error("PyMySQL not installed. Run: pip install pymysql")
            return False
        except Exception as e:
            logger.error(f"MySQL connection failed: {e}")
            return False
            
    def fetch_data(self, query: str = None, **kwargs) -> pd.DataFrame:
        if not self.connection:
            self.connect()
            
        if not query:
            query = """
            SELECT * FROM orders 
            WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
            ORDER BY created_at DESC
            """
            
        try:
            df = pd.read_sql_query(query, self.connection)
            logger.info(f"Fetched {len(df)} records from MySQL")
            return df
        except Exception as e:
            logger.error(f"MySQL query failed: {e}")
            return pd.DataFrame()

class APIConnector(DataConnector):
    """Generic REST API connector"""
    
    def connect(self) -> bool:
        # For APIs, we test with a simple request
        try:
            base_url = self.config.get('base_url')
            headers = self.config.get('headers', {})
            
            # Add API key if provided
            api_key = self.config.get('api_key')
            if api_key:
                headers['Authorization'] = f"Bearer {api_key}"
                
            response = requests.get(f"{base_url}/health", headers=headers, timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"API connection failed: {e}")
            return False
            
    def fetch_data(self, endpoint: str = None, **kwargs) -> pd.DataFrame:
        base_url = self.config.get('base_url')
        headers = self.config.get('headers', {})
        
        # Add API key if provided
        api_key = self.config.get('api_key')
        if api_key:
            headers['Authorization'] = f"Bearer {api_key}"
            
        if not endpoint:
            endpoint = '/orders'
            
        try:
            # Add date filter for recent data
            params = {
                'start_date': (datetime.now() - timedelta(days=30)).isoformat(),
                'limit': kwargs.get('limit', 1000)
            }
            
            response = requests.get(f"{base_url}{endpoint}", 
                                  headers=headers, 
                                  params=params, 
                                  timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Handle different response formats
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                # Look for common data keys
                for key in ['data', 'results', 'orders', 'items']:
                    if key in data and isinstance(data[key], list):
                        df = pd.DataFrame(data[key])
                        break
                else:
                    df = pd.DataFrame([data])
            else:
                df = pd.DataFrame()
                
            logger.info(f"Fetched {len(df)} records from API")
            return df
            
        except Exception as e:
            logger.error(f"API fetch failed: {e}")
            return pd.DataFrame()

class ShopifyConnector(APIConnector):
    """Shopify-specific API connector"""
    
    def connect(self) -> bool:
        try:
            shop_name = self.config.get('shop_name')
            api_key = self.config.get('api_key')
            
            if not shop_name or not api_key:
                return False
                
            # Test with shop info endpoint
            url = f"https://{shop_name}.myshopify.com/admin/api/2023-10/shop.json"
            headers = {'X-Shopify-Access-Token': api_key}
            
            response = requests.get(url, headers=headers, timeout=10)
            return response.status_code == 200
            
        except Exception as e:
            logger.error(f"Shopify connection failed: {e}")
            return False
            
    def fetch_data(self, resource: str = 'orders', **kwargs) -> pd.DataFrame:
        shop_name = self.config.get('shop_name')
        api_key = self.config.get('api_key')
        
        try:
            # Fetch recent orders
            url = f"https://{shop_name}.myshopify.com/admin/api/2023-10/{resource}.json"
            headers = {'X-Shopify-Access-Token': api_key}
            
            # Get orders from last 30 days
            created_at_min = (datetime.now() - timedelta(days=30)).isoformat()
            params = {
                'created_at_min': created_at_min,
                'limit': kwargs.get('limit', 250),
                'status': 'any'
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            orders = data.get('orders', [])
            
            # Flatten order data for analysis
            flattened_orders = []
            for order in orders:
                base_order = {
                    'order_id': order.get('id'),
                    'order_number': order.get('order_number'),
                    'created_at': order.get('created_at'),
                    'updated_at': order.get('updated_at'),
                    'total_price': float(order.get('total_price', 0)),
                    'subtotal_price': float(order.get('subtotal_price', 0)),
                    'total_tax': float(order.get('total_tax', 0)),
                    'currency': order.get('currency'),
                    'financial_status': order.get('financial_status'),
                    'fulfillment_status': order.get('fulfillment_status'),
                    'customer_id': order.get('customer', {}).get('id') if order.get('customer') else None,
                    'customer_email': order.get('customer', {}).get('email') if order.get('customer') else None,
                    'shipping_country': order.get('shipping_address', {}).get('country') if order.get('shipping_address') else None,
                    'shipping_city': order.get('shipping_address', {}).get('city') if order.get('shipping_address') else None
                }
                
                # Add line items
                for item in order.get('line_items', []):
                    item_data = base_order.copy()
                    item_data.update({
                        'product_id': item.get('product_id'),
                        'variant_id': item.get('variant_id'),
                        'product_title': item.get('title'),
                        'variant_title': item.get('variant_title'),
                        'quantity': item.get('quantity'),
                        'price': float(item.get('price', 0)),
                        'sku': item.get('sku'),
                        'vendor': item.get('vendor')
                    })
                    flattened_orders.append(item_data)
            
            df = pd.DataFrame(flattened_orders)
            logger.info(f"Fetched {len(df)} order items from Shopify")
            return df
            
        except Exception as e:
            logger.error(f"Shopify fetch failed: {e}")
            return pd.DataFrame()

class DataConnectorManager:
    """Manages multiple data connectors"""
    
    def __init__(self):
        self.connectors = {}
        self.config_file = 'config/data_connectors.json'
        self.load_config()
        
    def load_config(self):
        """Load connector configurations"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    
                for name, conn_config in config.get('connectors', {}).items():
                    self.add_connector(name, conn_config)
                    
            except Exception as e:
                logger.error(f"Failed to load connector config: {e}")
                
    def save_config(self):
        """Save connector configurations"""
        os.makedirs('config', exist_ok=True)
        
        config = {
            'connectors': {},
            'last_updated': datetime.now().isoformat()
        }
        
        for name, connector in self.connectors.items():
            # Don't save sensitive data like passwords
            safe_config = connector.config.copy()
            if 'password' in safe_config:
                safe_config['password'] = '***'
            if 'api_key' in safe_config:
                safe_config['api_key'] = '***'
                
            config['connectors'][name] = {
                'type': connector.__class__.__name__,
                'config': safe_config
            }
            
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
            
    def add_connector(self, name: str, config: Dict[str, Any]) -> bool:
        """Add a new data connector"""
        try:
            connector_type = config.get('type', 'API')
            connector_config = config.get('config', {})
            
            if connector_type == 'SQLite':
                connector = SQLiteConnector(connector_config)
            elif connector_type == 'PostgreSQL':
                connector = PostgreSQLConnector(connector_config)
            elif connector_type == 'MySQL':
                connector = MySQLConnector(connector_config)
            elif connector_type == 'Shopify':
                connector = ShopifyConnector(connector_config)
            elif connector_type == 'API':
                connector = APIConnector(connector_config)
            else:
                logger.error(f"Unknown connector type: {connector_type}")
                return False
                
            self.connectors[name] = connector
            logger.info(f"Added connector: {name} ({connector_type})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add connector {name}: {e}")
            return False
            
    def test_connector(self, name: str) -> Dict[str, Any]:
        """Test a specific connector"""
        if name not in self.connectors:
            return {
                'success': False,
                'message': f'Connector {name} not found'
            }
            
        return self.connectors[name].test_connection()
        
    def fetch_data(self, name: str, **kwargs) -> pd.DataFrame:
        """Fetch data from a specific connector"""
        if name not in self.connectors:
            logger.error(f"Connector {name} not found")
            return pd.DataFrame()
            
        return self.connectors[name].fetch_data(**kwargs)
        
    def list_connectors(self) -> List[Dict[str, Any]]:
        """List all configured connectors"""
        result = []
        for name, connector in self.connectors.items():
            result.append({
                'name': name,
                'type': connector.__class__.__name__,
                'status': 'configured'
            })
        return result
        
    def sync_data(self, connector_name: str, target_table: str = None) -> Dict[str, Any]:
        """Sync data from connector to local storage"""
        try:
            df = self.fetch_data(connector_name)
            
            if df.empty:
                return {
                    'success': False,
                    'message': 'No data fetched from connector'
                }
                
            # Save to processed data directory
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"sync_{connector_name}_{timestamp}.csv"
            filepath = os.path.join('data', 'processed', filename)
            
            os.makedirs('data/processed', exist_ok=True)
            df.to_csv(filepath, index=False)
            
            return {
                'success': True,
                'message': f'Synced {len(df)} records',
                'records': len(df),
                'file': filepath,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Data sync failed: {e}")
            return {
                'success': False,
                'message': f'Sync failed: {str(e)}'
            }

# Global connector manager instance
connector_manager = DataConnectorManager()