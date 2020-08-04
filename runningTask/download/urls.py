from django.urls import path

from download.controllers.download import (
    DownloadStartController,
    DownloadPauseController,
    DownloadResumeController,
    DownloadProgressController,
    DownloadTerminateController,
)

app_name = "download"

urlpatterns = [
    path("start", DownloadStartController.as_view(), name="download_start"),
    path("pause", DownloadPauseController.as_view(), name="download_pause"),
    path("resume", DownloadResumeController.as_view(), name="download_resume"),
    path(
        "terminate", DownloadTerminateController.as_view(), name="download_terminate",
    ),
    path("progress", DownloadProgressController.as_view(), name="download_progress"),
]
