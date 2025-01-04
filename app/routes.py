from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.firebase_config import save_poll, get_poll, save_vote, get_results
from app.utils import generate_poll_id, generate_admin_code

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('create_poll.html', show_your_polls=True)

@main.route('/create_poll', methods=['POST'])
def create_poll():
    question = request.form.get('question')
    options = request.form.getlist('options')
    
    if not question or len(options) < 2:
        flash('Please provide a question and at least two options')
        return redirect(url_for('main.index'))
    
    poll_id = generate_poll_id()
    admin_code = generate_admin_code()
    
    poll_data = {
        'question': question,
        'options': options,
        'admin_code': admin_code,
        'votes': {}
    }
    
    save_poll(poll_id, poll_data)
    
    return render_template('poll_created.html', 
                         poll_id=poll_id, 
                         admin_code=admin_code,
                         poll_url=url_for('main.view_poll', poll_id=poll_id, _external=True))

@main.route('/poll/<poll_id>')
def view_poll(poll_id):
    poll = get_poll(poll_id)
    if not poll:
        flash('Poll not found')
        return redirect(url_for('main.index'))
    return render_template('poll.html', poll=poll, poll_id=poll_id)

@main.route('/vote/<poll_id>', methods=['POST'])
def submit_vote(poll_id):
    option = request.form.get('option')
    if not option:
        flash('Please select an option')
        return redirect(url_for('main.view_poll', poll_id=poll_id))
    
    save_vote(poll_id, option)
    flash('Vote submitted successfully!')
    return redirect(url_for('main.view_poll', poll_id=poll_id))

@main.route('/privacy')
def privacy():
    return render_template('privacy.html')

@main.route('/results')
def view_results():
    poll_id = request.args.get('poll_id')
    admin_code = request.args.get('admin_code')
    
    if not poll_id or not admin_code:
        flash('Please provide both poll ID and admin code')
        return redirect(url_for('main.index'))
    
    poll = get_poll(poll_id)
    if not poll or poll['admin_code'] != admin_code:
        flash('Invalid poll ID or admin code')
        return redirect(url_for('main.index'))
    
    results = get_results(poll_id)
    return render_template('results.html', poll=poll, results=results)
