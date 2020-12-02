
def toggle_complete(task):
    task.is_completed = not task.is_completed
    task.save(update_fields=['is_completed'])
