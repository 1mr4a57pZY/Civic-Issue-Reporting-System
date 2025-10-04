from datetime import datetime
import pytz

def serialize_report(report):
    """
    Convert a SQLAlchemy Report object to a JSON-serializable dictionary.
    Handles all relationships and datetime objects properly.
    """
    # Convert datetime objects to ISO format strings
    def datetime_to_iso(dt):
        if dt:
            # Convert to UTC for consistent JSON serialization
            if dt.tzinfo:
                dt = dt.astimezone(pytz.UTC)
            else:
                dt = pytz.UTC.localize(dt)
            return dt.isoformat()
        return None

    # Convert media strings to lists
    def media_to_list(media_str):
        if media_str:
            return media_str.split(';')
        return []

    # Serialize user (basic info only)
    user_data = None
    if report.user:
        user_data = {
            'id': report.user.id,
            'name': report.user.name,
            'email': report.user.email,
            'mobile': report.user.mobile
        }

    # Serialize updates
    updates_data = []
    for update in report.updates:
        updates_data.append({
            'id': update.id,
            'status': update.status,
            'comment': update.comment,
            'photo': media_to_list(update.photo),
            'created_at': datetime_to_iso(update.created_at)
        })

    # Serialize feedbacks
    feedbacks_data = []
    for feedback in report.feedbacks:
        feedbacks_data.append({
            'id': feedback.id,
            'rating': feedback.rating,
            'comment': feedback.comment,
            'created_at': datetime_to_iso(feedback.created_at)
        })

    # Main report data
    report_dict = {
        'id': report.id,
        'title': report.title,
        'short_description': report.short_description,
        'description': report.description,
        'location': report.location,
        'latitude': report.latitude,
        'longitude': report.longitude,
        'status': report.status,
        'department': report.department,
        'photo': media_to_list(report.photo),  # Convert to list
        'media': media_to_list(report.media),  # Convert to list
        'created_at': datetime_to_iso(report.created_at),
        'updated_at': datetime_to_iso(report.updated_at),
        'user_id': report.user_id,
        'user': user_data,
        'updates': updates_data,
        'feedbacks': feedbacks_data
    }

    return report_dict

def serialize_reports(reports):
    """
    Convert a list of SQLAlchemy Report objects to JSON-serializable dictionaries.
    """
    return [serialize_report(report) for report in reports]
