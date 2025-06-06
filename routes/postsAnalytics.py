"""
This module contains the code for the posts analytics page.
"""

from modules import (
    ANALYTICS,  # A constant variable to check analytics True or False
    DB_POSTS_ROOT,  # A constant for the path to the posts database
    getAnalyticsPageTrafficGraphData,  # Function to get post traffic graph data
    getAnalyticsPageOSGraphData,  # Function to get post os graph data
    Blueprint,  # A class for creating Flask blueprints
    Log,  # A class for logging messages
    render_template,  # A function for rendering Jinja templates
    request,  # A Request handling module
    session,  # Session management module
    sqlite3,  # A module for working with SQLite databases
)

analyticsBlueprint = Blueprint(
    "analytics", __name__
)  # Create a blueprint for the analytics page


@analyticsBlueprint.route(
    "/analytics/posts/<urlID>"
)  # Define a route for the posts analytics page with a dynamic urlID parameter
def analyticsPost(urlID):
    """
    This function is used to render the post analytics page.

    :param urlID: The urlID of the post.
    :type urlID: str
    :return: The rendered analytics post page.
    :rtype: flask.Response
    """
    match ANALYTICS:
        case True:
            match "userName" in session:
                case True:
                    # Use the sqlite3 module to connect to the database and get a cursor object
                    connection = sqlite3.connect(DB_POSTS_ROOT)
                    connection.set_trace_callback(
                        Log.database
                    )  # Set the trace callback for the connection
                    cursor = connection.cursor()
                    # Query the posts database for all post url IDs
                    cursor.execute("select urlID from posts")
                    posts = str(cursor.fetchall())

                    # Check if the requested post ID exists in the posts database
                    match urlID in posts:
                        case True:
                            # Log a message indicating that the post is found
                            Log.success(f'post: "{urlID}" loaded')

                            Log.database(
                                f"Connecting to '{DB_POSTS_ROOT}' database"
                            )  # Log the database connection is started
                            # Connect to the posts database
                            connection = sqlite3.connect(DB_POSTS_ROOT)
                            connection.set_trace_callback(
                                Log.database
                            )  # Set the trace callback for the connection
                            cursor = connection.cursor()

                            # Query the posts database for the post with the matching url ID
                            cursor.execute(
                                """select * from posts where urlID = ? """,
                                [(urlID)],
                            )
                            post = cursor.fetchone()

                            # Fetch all the results as a list inside list
                            todaysVisitorData = getAnalyticsPageTrafficGraphData(
                                postID=post[0], hours=24
                            )  # if no params are passed except postID function will return last 48 hours of data
                            todaysVisitor = 0  # Initialize a variable for storing the today's total number of views
                            for views in (
                                todaysVisitorData
                            ):  # Loop through each list in the list
                                todaysVisitor += int(
                                    views[1]
                                )  # Add the second element of the list (the view count) to the total visitor

                            # os graph data
                            osGraphData = getAnalyticsPageOSGraphData(post[0])

                            return render_template(
                                "postsAnalytics.html.jinja",
                                post=post,
                                todaysVisitor=todaysVisitor,
                                osGraphData=osGraphData,
                            )

                        case False:
                            Log.error(
                                f"{request.remote_addr} tried to reach unknown post"
                            )  # Log a message with level 1 indicating the post is not found
                            # Render the 404 template if the post ID does not exist
                            return render_template("notFound.html.jinja")

                case False:
                    Log.error(
                        f"{request.remote_addr} tried to reach unknown post"
                    )  # Log a message with level 1 indicating the post is not found
                    # Render the 404 template if the post ID does not exist
                    return render_template("notFound.html.jinja")

        case False:
            Log.error(
                f"{request.remote_addr} tried to reach unknown post"
            )  # Log a message with level 1 indicating the post is not found
            # Render the 404 template if the post ID does not exist
            return render_template("notFound.html.jinja")
