# FastAPI Blogging APIs

These are the FastAPI endpoints for a blogging application. Below are the available routes and their descriptions:

## User Routes

### Register User
- **Method:** `POST`
- **Endpoint:** `/register`
- **Description:** Register a new user.
- **Parameters:**
  - `userInfo (registrationModel)`: User registration information.
- **Returns:**
  - A dictionary containing information about the new user and a token.
- **Raises:**
  - `HTTPException`: If there's a validation error or the user already exists.

### Login User
- **Method:** `POST`
- **Endpoint:** `/login`
- **Description:** Login with user credentials.
- **Parameters:**
  - `userInfo (loginModel)`: User login information.
- **Returns:**
  - A dictionary containing a success message, token, and user information.
- **Raises:**
  - `HTTPException`: If there's a validation error, incorrect email/password, or user not found.

### Verify User
- **Method:** `GET`
- **Endpoint:** `/verifyUser`
- **Description:** Verify user authentication.
- **Parameters:**
  - `credentials (HTTPAuthorizationCredentials)`: User credentials for authentication.

### Get User
- **Method:** `GET`
- **Endpoint:** `/getUser`
- **Description:** Get user information.
- **Parameters:**
  - `credentials (HTTPAuthorizationCredentials)`: User credentials for authentication.

### Update User
- **Method:** `PUT`
- **Endpoint:** `/updateUser`
- **Description:** Update user information.
- **Parameters:**
  - `credentials (HTTPAuthorizationCredentials)`: User credentials for authentication.
  - `userInfo (updateUserModel)`: Updated user information.
- **Returns:**
  - A message confirming the successful update.
- **Raises:**
  - `HTTPException`: If there's an internal server error.

### Delete User
- **Method:** `DELETE`
- **Endpoint:** `/deleteUser`
- **Description:** Delete a user.
- **Parameters:**
  - `credentials (HTTPAuthorizationCredentials)`: User credentials for authentication.
- **Returns:**
  - A message confirming the successful deletion.
- **Raises:**
  - `HTTPException`: If there's an internal server error.

## Post Routes

### Add Post
- **Method:** `POST`
- **Endpoint:** `/addPost`
- **Description:** Add a new post to the blog.
- **Parameters:**
  - `credentials (HTTPAuthorizationCredentials)`: User credentials for authentication.
  - `postInfo (AddPostModel)`: Information of the post to be added.
- **Returns:**
  - A dictionary containing a success message and details of the newly added post.
- **Raises:**
  - `HTTPException`: If there's an internal server error.

### Get All Posts
- **Method:** `GET`
- **Endpoint:** `/getAllPost/{limit}`
- **Description:** Get all posts.
- **Parameters:**
  - `limit (int)`: Maximum number of posts to retrieve.
  - `credentials (HTTPAuthorizationCredentials)`: User credentials for authentication.
- **Returns:**
  - A dictionary containing details of all the retrieved posts.
- **Raises:**
  - `HTTPException`: If there's an internal server error.

### Get Single Post
- **Method:** `GET`
- **Endpoint:** `/singlePost/{postId}`
- **Description:** Get a single post by its postId.
- **Parameters:**
  - `postId (str)`: Identifier of the post to retrieve.
  - `credentials (HTTPAuthorizationCredentials)`: User credentials for authentication.
- **Returns:**
  - A dictionary containing details of the retrieved post.
- **Raises:**
  - `HTTPException`: If the post is not found or there's an internal server error.

### Delete Post
- **Method:** `DELETE`
- **Endpoint:** `/deletePost/{postId}`
- **Description:** Delete a post by its postId.
- **Parameters:**
  - `postId (str)`: Identifier of the post to delete.
  - `credentials (HTTPAuthorizationCredentials)`: User credentials for authentication.
- **Returns:**
  - A message confirming the successful deletion.
- **Raises:**
  - `HTTPException`: If there's an internal server error.

### Update Post
- **Method:** `PUT`
- **Endpoint:** `/updatePost/{postId}`
- **Description:** Update a post by its postId.
- **Parameters:**
  - `postId (str)`: Identifier of the post to update.
  - `postInfo (AddPostModel)`: Updated information of the post.
  - `credentials (HTTPAuthorizationCredentials)`: User credentials for authentication.
- **Returns:**
  - A message confirming the successful update.
- **Raises:**
  - `HTTPException`: If there's an internal server error.

### Search Post
- **Method:** `GET`
- **Endpoint:** `/searchPost/{search_query}`
- **Description:** Search posts by a search query.
- **Parameters:**
  - `search_query (str)`: Search query to match against post titles and content.
  - `credentials (HTTPAuthorizationCredentials)`: User credentials for authentication.
- **Returns:**
  - A dictionary containing details of the matching posts.
- **Raises:**
  - `HTTPException`: If there's an internal server error.

### Get Specific User Posts
- **Method:** `GET`
- **Endpoint:** `/specificUserPosts/{limit}`
- **Description:** Get posts of a specific user.
- **Parameters:**
  - `limit (int)`: Maximum number of posts to retrieve.
  - `credentials (HTTPAuthorizationCredentials)`: User credentials for authentication.
- **Returns:**
  - A dictionary containing details of the specific user posts.
- **Raises:**
  - `HTTPException`: If there's an internal server error.

### Add Comment
- **Method:** `POST`
- **Endpoint:** `/addComment/{postId}`
- **Description:** Add a comment to a post.
- **Parameters:**
  - `postId (str)`: Identifier of the post to add a comment to.
  - `content (Comment)`: Content of the comment to be added.
  - `credentials (HTTPAuthorizationCredentials)`: User credentials for authentication.
- **Returns:**
  - A message confirming the successful addition of the comment.
- **Raises:**
  - `HTTPException`: If there's an internal server error.

### Remove Comment
- **Method:** `POST`
- **Endpoint:** `/removeComment/{postId}`
- **Description:** Remove a comment from a post.
- **Parameters:**
  - `postId (str)`: Identifier of the post to remove a comment from.
  - `commentData (CommentUniquId)`: Identifier of the comment to be removed.
  - `credentials (HTTPAuthorizationCredentials)`: User credentials for authentication.
- **Returns:**
  - A message confirming the successful removal of the comment.
- **Raises:**
  - `HTTPException`: If there's an internal server error.

### Get Comments
- **Method:** `GET`
- **Endpoint:** `/getComment/{postId}`
- **Description:** Get comments of a post by postId.
- **Parameters:**
  - `postId (str)`: Identifier of the post to retrieve comments from.
  - `credentials (HTTPAuthorizationCredentials)`: User credentials for authentication.
- **Returns:**
  - A dictionary containing details of the comments for the specified post.
- **Raises:**
  - `HTTPException`: If there's an internal server error.

### Add or Remove Like
- **Method:** `POST`
- **Endpoint:** `/addOrRemoveLike/{postId}`
- **Description:** Add or remove a like from a post.
- **Parameters:**
  - `postId (str)`: Identifier of the post to add or remove a like from.
  - `credentials (HTTPAuthorizationCredentials)`: User credentials for authentication.
- **Returns:**
  - A message confirming the successful addition or removal of the like.
- **Raises:**
  - `HTTPException`: If there's an internal server error.

### Get Post Likes
- **Method:** `GET`
- **Endpoint:** `/getPostLike/{postId}`
- **Description:** Get likes of a post by postId.
- **Parameters:**
  - `postId (str)`: Identifier of the post to retrieve likes from.
  - `credentials (HTTPAuthorizationCredentials)`: User credentials for authentication.
- **Returns:**
  - A dictionary containing details of the likes for the specified post.
- **Raises:**
  - `HTTPException`: If there's an internal server error.

---

**Note:** Replace `{}` with appropriate values in the route parameters.
