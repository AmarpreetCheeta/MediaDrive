from django.urls import path
from app.views import *


urlpatterns = [
	path('',HomeView.as_view(),name='home'),
	path('starred/',StarredView.as_view(),name='starred'),
	path('folder/<int:pk>/',FoldersView.as_view(),name='folders'),
	path('user/change_password/',ChangePassword,name='change_password'),

	path('q/',SearchBar.as_view(),name='search'),

	path('create_folder/',CreateFolder,name='folders_create'),
	path('starred_folder/<folder_name>/',FoldersStarredView,name='starred_folder'),
	path('second_starred_folder/<folder_name>/',SecondFoldersStarredView,name='second_starred_folder'),
	path('remove_forever_folder/<int:pk>/',RemoveForeverFolders,name='remove_forever_folder'),

	path('remove_forever_folder_from_starred/<int:pk>/',RemoveForeverFolderFromStarred,name='remove_forever_folder_from_starred'),
	path('remove_forever_files_from_starred/<int:pk>/',RemoveForeverFilesFromStarred,name='remove_forever_files_from_starred'),
	path('remove_forever_folders_files_from_starred/<int:pk>/',RemoveForeverFoldersFilesFromStarred,name='remove_forever_folders_files_from_starred'),

	path('starred_files/<int:pk>/',FilesStarredView,name='starred_files'),
	path('starred_files_move_to_folder/<int:pk>/',StarredFileMoveToFolderView,name='starred_files_move_to_folder'),
	path('second_starred_files_move_to_folder/<int:pk>/',SecondStarredFileMoveToFolderView,name='second_starred_files_move_to_folder'),

	path('second_starred_files/<int:pk>/',SecondFilesStarredView,name='second_starred_files'),
	path('remove_files/<int:pk>/',RemoveForeverFiles,name='remove_files'),
	path('remove_files_from_folders/<int:pk>/',RemoveForeverFilesFromFolder,name='remove_files_from_folders'),

	path('file_move_to_folder/<int:pk>/',FileMoveToFolder,name='file_move_to_folder'),

	path('user/account/',AccountView.as_view(),name='account'),

	path('delete_profile_img/',ProfileImageDelete,name='delete_profile_img'),

	path('account_delete/<phone>/',UserAccountDeleteClass.as_view(),name='delete_account'),

	path('logout/',LogoutClass.as_view(),name='logout'),
]