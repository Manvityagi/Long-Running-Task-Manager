from django.urls import path

from upload.controllers.upload import (
    UploadStartController,
    UploadPauseController,
    UploadResumeController,
    UploadProgressController,
    UploadTerminateController,
    TableExistController,
)

app_name = "upload"

urlpatterns = [
    path("start", UploadStartController.as_view(), name="upload_start"),
    path("pause", UploadPauseController.as_view(), name="upload_pause"),
    path("resume", UploadResumeController.as_view(), name="upload_resume"),
    path("terminate", UploadTerminateController.as_view(), name="upload_terminate",),
    path("progress", UploadProgressController.as_view(), name="upload_progress"),
    path("exists/<str:userid>", TableExistController.as_view(), name="table_exists"),
]
