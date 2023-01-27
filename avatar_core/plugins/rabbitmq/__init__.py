from avatar_core.plugins.rabbitmq.plugin import RabbitMQ, RabbitMQPlugin, depends_rabbitmq, init_rabbitmq
from avatar_core.plugins.rabbitmq.settings import RabbitMQSettings

__all__ = ["init_rabbitmq", "RabbitMQSettings", "depends_rabbitmq", "RabbitMQ", "RabbitMQPlugin"]
