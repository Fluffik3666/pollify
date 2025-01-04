from firebase_admin import db

def save_poll(poll_id, poll_data):
    ref = db.reference('polls')
    ref.child(poll_id).set(poll_data)

def get_poll(poll_id):
    ref = db.reference(f'polls/{poll_id}')
    return ref.get()

def save_vote(poll_id, option):
    ref = db.reference(f'polls/{poll_id}/votes')
    ref.push().set(option)

def get_results(poll_id):
    ref = db.reference(f'polls/{poll_id}/votes')
    votes = ref.get()
    if not votes:
        return {}
    results = {}
    for vote in votes.values():
        results[vote] = results.get(vote, 0) + 1
    return results