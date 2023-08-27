import os

def create_upload_directory(upload_dir):
    if not os.path.exists(upload_dir):
        try:
            # Create the upload directory
            os.makedirs(upload_dir)
            print(f"Upload directory created: {upload_dir}")
            return True
        except OSError as e:
            print(f"Error creating upload directory: {e}")
            return False
    else:
        print(f"Upload directory already exists: {upload_dir}")
        return True