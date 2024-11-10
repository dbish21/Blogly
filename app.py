# ... database configuration ...

@app.route('/')
def root():
    """Homepage redirects to list of users."""
    # Redirect root URL to users page for better UX - avoids empty homepage
    return redirect("/users")

@app.route('/users')
def users_index():
    """Show a page with info on all users"""
    # Order users by last name then first name for alphabetical listing
    # Using order_by() for consistent, sorted display
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)

@app.route("/users/new", methods=["POST"])
def users_new():
    """Handle form submission for creating a new user"""
    # Handle optional image_url - if empty string provided, store as None
    # This prevents empty strings in database and provides cleaner data
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    # Add and commit in two steps to ensure proper transaction handling
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Handle form submission for updating an existing user"""
    # get_or_404 used instead of get() to automatically handle missing users
    user = User.query.get_or_404(user_id)
    
    # Update user attributes directly from form data
    # No validation here - would be good to add in production
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    # For updates, add() is optional but included for consistency
    # SQLAlchemy will detect the change and update accordingly
    db.session.add(user)
    db.session.commit()

    return redirect("/users") 