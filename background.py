from gooutsafe import create_app_with_celery

app, celery = create_app_with_celery()
try:
    import gooutsafe.tasks.contact_tracing
    import gooutsafe.tasks.health_authority_tasks
except ImportError as e:
    raise RuntimeError('Cannot start background due to import error')
