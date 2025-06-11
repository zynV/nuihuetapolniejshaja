import sqlite3
import logging
from datetime import datetime
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

def init_db():
    """Инициализация базы данных"""
    try:
        conn = sqlite3.connect('database/auth.db')
        cursor = conn.cursor()
        
        # Создание таблицы users
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            patreon_id TEXT PRIMARY KEY,
            telegram_id INTEGER,
            email TEXT,
            access_token TEXT,
            tier TEXT,
            joined_channel BOOLEAN DEFAULT FALSE,
            expires_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        logger.info("База данных успешно инициализирована")
    except Exception as e:
        logger.error(f"Ошибка при инициализации базы данных: {e}")
        raise
    finally:
        conn.close()

def save_user_data(user_data: Dict[str, Any]) -> bool:
    """Сохранение данных пользователя"""
    try:
        conn = sqlite3.connect('database/auth.db')
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT OR REPLACE INTO users 
        (patreon_id, telegram_id, email, access_token, tier, joined_channel, expires_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_data['patreon_id'],
            user_data['telegram_id'],
            user_data['email'],
            user_data['access_token'],
            user_data.get('tier'),
            False,
            user_data.get('expires_at')
        ))
        
        conn.commit()
        logger.info(f"Данные пользователя {user_data['patreon_id']} успешно сохранены")
        return True
    except Exception as e:
        logger.error(f"Ошибка при сохранении данных пользователя: {e}")
        return False
    finally:
        conn.close()

def get_user_by_patreon_id(patreon_id: str) -> Optional[Dict[str, Any]]:
    """Получение данных пользователя по Patreon ID"""
    try:
        conn = sqlite3.connect('database/auth.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE patreon_id = ?', (patreon_id,))
        user = cursor.fetchone()
        
        if user:
            return {
                'patreon_id': user[0],
                'telegram_id': user[1],
                'email': user[2],
                'access_token': user[3],
                'tier': user[4],
                'joined_channel': bool(user[5]),
                'expires_at': user[6]
            }
        return None
    except Exception as e:
        logger.error(f"Ошибка при получении данных пользователя: {e}")
        return None
    finally:
        conn.close()

def update_user_tier(patreon_id: str, tier: str) -> bool:
    """Обновление уровня подписки пользователя"""
    try:
        conn = sqlite3.connect('database/auth.db')
        cursor = conn.cursor()
        
        cursor.execute('UPDATE users SET tier = ? WHERE patreon_id = ?', (tier, patreon_id))
        conn.commit()
        
        logger.info(f"Уровень подписки пользователя {patreon_id} обновлен на {tier}")
        return True
    except Exception as e:
        logger.error(f"Ошибка при обновлении уровня подписки: {e}")
        return False
    finally:
        conn.close()

def mark_user_joined(patreon_id: str) -> bool:
    """Отметка о вступлении пользователя в канал"""
    try:
        conn = sqlite3.connect('database/auth.db')
        cursor = conn.cursor()
        
        cursor.execute('UPDATE users SET joined_channel = TRUE WHERE patreon_id = ?', (patreon_id,))
        conn.commit()
        
        logger.info(f"Пользователь {patreon_id} отмечен как вступивший в канал")
        return True
    except Exception as e:
        logger.error(f"Ошибка при отметке вступления в канал: {e}")
        return False
    finally:
        conn.close()
