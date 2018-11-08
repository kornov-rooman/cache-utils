

def pytest_configure():
    from aiocache import caches

    caches.set_config({
        'default': {
            'namespace': 'cache-utils-test',
            'cache': 'aiocache.SimpleMemoryCache',
            'serializer': {
                'class': 'aiocache.serializers.PickleSerializer',
                # 'class': 'aiocache.serializers.MsgPackSerializer',
            }
        }
    })
