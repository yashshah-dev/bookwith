class AnnotationNotFoundError(Exception):
    """Exception raised when the specified annotation is not found."""

    def __init__(self, annotation_id: str) -> None:
        self.annotation_id = annotation_id
        super().__init__(f"Annotation with id '{annotation_id}' not found.")
