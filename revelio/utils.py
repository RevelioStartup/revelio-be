def get_validation_error_detail(e):
    """
    Extract and format the error message from a ValidationError.
    Args:
    e (ValidationError): The exception raised.

    Returns:
    str: A formatted string containing the error message.
    """
    if hasattr(e, 'detail'):
        if isinstance(e.detail, dict) or isinstance(e.detail, list):
            # Flatten the error message details
            error_messages = []
            for detail in (e.detail.values() if isinstance(e.detail, dict) else e.detail):
                if isinstance(detail, list):
                    error_messages.extend([str(msg) for msg in detail])
                else:
                    error_messages.append(str(detail))
            error_message = '; '.join(error_messages)
        else:
            error_message = str(e.detail)
    else:
        error_message = str(e)
    return error_message
