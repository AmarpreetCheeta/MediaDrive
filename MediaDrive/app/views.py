from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib import messages
from app.models import *
from app.forms import *
from django.contrib.auth.views import *


def SignUp(request):
	if not request.user.is_authenticated:
		if request.method == 'POST':
			form = AccountCreationForm(request.POST)
			if form.is_valid():
				user = form.save()
				login(request, user)
				return redirect('home')
			else:
				messages.success(request, "Something is wrong, Please try once again.")
		else:
			form = AccountCreationForm()
			return render(request, 'signup.html',{'forms':form})
	else:
		return redirect('home')


def LogIn(request):
	if not request.user.is_authenticated:
		if request.method == 'POST':
			form = AuthenticationUserForm(request=request, data=request.POST)
			if form.is_valid():
				us = form.cleaned_data['username']
				pas = form.cleaned_data['password']
				log = authenticate(username=us,password=pas)
				if log is not None:
					login(request, log)
					return redirect('home')
		else:
			form = AuthenticationUserForm()
		return render(request, 'login.html',{'forms':form})
	else:
		return redirect('home')


class SearchBar(TemplateView):
	def get(self, request):
		if request.user.is_authenticated:
			starred_counts = 0
			folders_data = DuplicateFolderModel.objects.filter(user=request.user)
			files_data = DuplicateFilesModel.objects.filter(user=request.user)
			starred_data = StarredFolderModel.objects.filter(user=request.user)
			starred_files_data = StarredFilesModel.objects.filter(user=request.user)
			starred_files_move_to_folder = StarredFileMoveToFolderModel.objects.filter(user=request.user)
			starred_counts = starred_data.count() + starred_files_data.count() + starred_files_move_to_folder.count()
			search_data = request.GET.get('search_for')
			folder_key = FolderModel.objects.filter(user=request.user,folder_name__icontains=search_data)
			files_key = FilesModel.objects.filter(user=request.user,file__icontains=search_data)
			context = {'folders_data':folders_data,'starred_counts':starred_counts,'files_data':files_data,
			'folder_key':folder_key,'files_key':files_key}
			return render(request, 'search.html',context)
		else:
			return redirect('login')


class HomeView(TemplateView):
	def get(self, request):
		if request.user.is_authenticated:
			starred_counts = 0
			folders_data = DuplicateFolderModel.objects.filter(user=request.user)
			starred_data = StarredFolderModel.objects.filter(user=request.user)
			starred_files_data = StarredFilesModel.objects.filter(user=request.user)
			starred_files_move_to_folder = StarredFileMoveToFolderModel.objects.filter(user=request.user)
			starred_counts = starred_data.count() + starred_files_data.count() + starred_files_move_to_folder.count()
			files_data = DuplicateFilesModel.objects.filter(user=request.user)
			file_form = FilesCreateForm()
			context = {'folders_data':folders_data,'starred_counts':starred_counts,'files_data':files_data,
			'file_form':file_form}
			return render(request, 'home.html',context)
		else:
			return redirect('login')

	def post(self, request):
		if request.user.is_authenticated:
			file_form = FilesCreateForm(data=request.POST, files=request.FILES)
			if file_form.is_valid():
				file = file_form.cleaned_data['file']
				reg = FilesModel(user=request.user,file=file)
				reg.save()
				duplicate_file = DuplicateFilesModel(user=request.user, files_id=reg)
				duplicate_file.save()
				return redirect('home')
		else:
			return redirect('login')


class StarredView(TemplateView):
	def get(self, request):
		if request.user.is_authenticated:
			starred_counts = 0
			folders_data = DuplicateFolderModel.objects.filter(user=request.user)
			starred_data = StarredFolderModel.objects.filter(user=request.user)
			starred_files_data = StarredFilesModel.objects.filter(user=request.user)
			starred_files_move_to_folder = StarredFileMoveToFolderModel.objects.filter(user=request.user)
			starred_counts = starred_data.count() + starred_files_data.count() + starred_files_move_to_folder.count()
			context = {'starred_counts':starred_counts,'starred_data':starred_data,'starred_files_data':starred_files_data,
			'starred_files_move_to_folder':starred_files_move_to_folder,'folders_data':folders_data}
			return render(request, 'starred.html',context)
		else:
			return redirect('login')


class FoldersView(TemplateView):
	def get(self, request, pk):
		if request.user.is_authenticated:
			folders_data = FolderModel.objects.get(pk=pk)
			folders_data2 = FolderModel.objects.filter(pk=pk)
			starred_counts = 0
			starred_data = StarredFolderModel.objects.filter(user=request.user)
			starred_files_data = StarredFilesModel.objects.filter(user=request.user)
			starred_files_move_to_folder = StarredFileMoveToFolderModel.objects.filter(user=request.user)
			starred_counts = starred_data.count() + starred_files_data.count() + starred_files_move_to_folder.count()
			moveTo_fileData = FilesMoveToFolderModel.objects.filter(folders=pk)
			file_form = FilesCreateForm()
			context = {'starred_counts':starred_counts,'moveTo_fileData':moveTo_fileData,'folders_data':folders_data2,
			'file_form':file_form}
			return render(request, 'folders.html',context)
		else:
			return redirect('login')

	def post(self, request, pk):
		if request.user.is_authenticated:
			file_form = FilesCreateForm(data=request.POST,files=request.FILES)
			if file_form.is_valid():
				file = file_form.cleaned_data['file']
				reg, create_files = FilesModel.objects.get_or_create(user=request.user,file=file)
				if create_files:
					folders_data = FolderModel.objects.get(pk=pk)
					file_move_to_folder = FilesMoveToFolderModel(user=request.user,files=reg,folders=folders_data)
					file_move_to_folder.save()
				return redirect('folders',folders_data.id)
		else:
			return redirect('login')


class AccountView(TemplateView):
	def get(self, request):
		if request.user.is_authenticated:
			form = UserUpdateForm(instance=request.user)
			starred_counts = 0
			starred_data = StarredFolderModel.objects.filter(user=request.user)
			starred_files_data = StarredFilesModel.objects.filter(user=request.user)
			starred_files_move_to_folder = StarredFileMoveToFolderModel.objects.filter(user=request.user)
			starred_counts = starred_data.count() + starred_files_data.count() + starred_files_move_to_folder.count()
			context = {'forms':form,'starred_counts':starred_counts}
			return render(request, 'account.html',context)
		else:
			return redirect('login')

	def post(self, request):
		if request.user.is_authenticated:
			form = UserUpdateForm(data=request.POST, files=request.FILES, instance=request.user)
			if form.is_valid():
				form.save()
				return redirect('account')
		else:
			return redirect('login')

def ProfileImageDelete(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			user_image = request.user.image
			user_image.delete()
			return redirect('account')
	else:
		return redirect('login')


# Folders 

def CreateFolder(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			folder_name = request.POST.get('folder_name')
			folder_data = FolderModel(user=request.user, folder_name=folder_name)
			folder_data.save()
			duplicate_folder_data = DuplicateFolderModel(user=request.user, folders=folder_data)
			duplicate_folder_data.save()
			return redirect('home')
	else:
		return redirect('login')


def FoldersStarredView(request,folder_name):
	if request.user.is_authenticated:
		if request.method == 'POST':
			folders_key = FolderModel.objects.get(folder_name=folder_name)
			starred, create_starred = StarredFolderModel.objects.get_or_create(user=request.user,folders=folders_key)
			if create_starred:
				folder_data = FolderModel.objects.get(folder_name=folder_name)
				folder_data.starred_folder = 'Starred'
				folder_data.save()
			else:
				starred.delete()
				folder_data = FolderModel.objects.get(folder_name=folder_name)
				folder_data.starred_folder = ''
				folder_data.save()
			return redirect('home')
	else:
		return redirect('login')

def SecondFoldersStarredView(request,folder_name):
	if request.user.is_authenticated:
		if request.method == 'POST':
			folders_key = FolderModel.objects.get(folder_name=folder_name)
			starred, create_starred = StarredFolderModel.objects.get_or_create(user=request.user,folders=folders_key)
			if create_starred:
				Starred.save()
				folder_data = FolderModel.objects.get(folder_name=folder_name)
				folder_data.starred_folder = 'Starred'
				folder_data.save()
			else:
				starred.delete()
				folder_data = FolderModel.objects.get(folder_name=folder_name)
				folder_data.starred_folder = ''
				folder_data.save()
			return redirect('starred')
	else:
		return redirect('login')


def RemoveForeverFolders(request, pk):
	if request.user.is_authenticated:
		if request.method == 'POST':
			folder_data = FolderModel.objects.get(pk=pk)
			folder_data.delete()
			return redirect('home')
	else:
		return redirect('login')


def RemoveForeverFolderFromStarred(request, pk):
	if request.user.is_authenticated:
		if request.method == 'POST':
			folders_data = FolderModel.objects.get(pk=pk)
			folders_data.delete()
			return redirect('starred')
	else:
		return redirect('login')

# End Folders

# Files

def RemoveForeverFilesFromStarred(request, pk):
	if request.user.is_authenticated:
		if request.method == 'POST':
			files_data = FilesModel.objects.get(pk=pk)
			files_data.delete()
			return redirect('starred')
	else:
		return redirect('login')


def RemoveForeverFoldersFilesFromStarred(request, pk):
	if request.user.is_authenticated:
		if request.method == 'POST':
			files_data = FilesModel.objects.get(pk=pk)
			file_move_to_folder = FilesMoveToFolderModel.objects.get(files=files_data)
			file_move_to_folder.delete()
			files_data.delete()
			return redirect('starred')
	else:
		return redirect('login')


def FilesStarredView(request, pk):
	if request.user.is_authenticated:
		if request.method == 'POST':
			files_key = FilesModel.objects.get(pk=pk)
			starred, create_starred = StarredFilesModel.objects.get_or_create(user=request.user,files=files_key)
			if create_starred:
				files_data = FilesModel.objects.get(pk=pk)
				files_data.starred_folder = 'Starred'
				files_data.save()
			else:
				starred.delete()
				files_data = FilesModel.objects.get(pk=pk)
				files_data.starred_folder = ''
				files_data.save()
			return redirect('home')
	else:
		return redirect('login')

def SecondFilesStarredView(request, pk):
	if request.user.is_authenticated:
		if request.method == 'POST':
			files_key = FilesModel.objects.get(pk=pk)
			starred = StarredFilesModel.objects.get(files=files_key)
			starred.delete()
			files_key.starred_folder = ''
			files_key.save()
			return redirect('starred')
	else:
		return redirect('login')

def RemoveForeverFiles(request, pk):
	if request.user.is_authenticated:
		if request.method == 'POST':
			files_data = FilesModel.objects.get(pk=pk)
			files_data.delete()
			return redirect('home')
	else:
		return redirect('login')

def RemoveForeverFilesFromFolder(request, pk):
	if request.user.is_authenticated:
		if request.method == 'POST':
			folder_id = request.POST.get('folders_id')
			folders_data = FolderModel.objects.get(pk=folder_id)
			files_data = FilesModel.objects.get(pk=pk)
			files_data.delete()
			return redirect('folders',folders_data.id)
	else:
		return redirect('login')

def FileMoveToFolder(request, pk):
	if request.user.is_authenticated:
		if request.method == 'POST':
			folder_key = request.POST.get('folders_key')
			folders_data = FolderModel.objects.get(pk=folder_key)
			files_data = FilesModel.objects.get(pk=pk)
			move_to, file_move_to_filder = FilesMoveToFolderModel.objects.get_or_create(user=request.user,files=files_data,folders=folders_data)
			if file_move_to_filder:
				duplicate_file = DuplicateFilesModel.objects.get(files_id=files_data)
				duplicate_file.delete()
				return redirect('home')
			else:
				duplicate_file = DuplicateFilesModel(user=request.user,files_id=files_data)
				duplicate_file.save()
				move_to.delete()
				return redirect('folders', folders_data.id)
	else:
		return redirect('login')


def StarredFileMoveToFolderView(request, pk):
	if request.user.is_authenticated:
		if request.method == 'POST':
			folder_id = request.POST.get('folderid_key')
			folders_data = FolderModel.objects.get(pk=folder_id)
			files_data = FilesModel.objects.get(pk=pk)
			moveTo, starred_files_move_to_folder = StarredFileMoveToFolderModel.objects.get_or_create(user=request.user,files=files_data,folders=folders_data)
			if starred_files_move_to_folder:
				files_data.starred_folder = 'Starred'
				files_data.save()
			else:
				moveTo.delete()
				files_data.starred_folder = ''
				files_data.save()
			return redirect('folders', folders_data.id)
	else:
		return redirect('login')


def SecondStarredFileMoveToFolderView(request, pk):
	if request.user.is_authenticated:
		if request.method == 'POST':
			files_data = FilesModel.objects.get(pk=pk)
			moveTo = StarredFileMoveToFolderModel.objects.get(files=files_data)
			moveTo.delete()
			files_data.starred_folder = ''
			files_data.save()
			return redirect('starred')
	else:
		return redirect('login')

# End File


def ChangePassword(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			form = ChangePasswordForm(request.user, request.POST)
			if form.is_valid():
				user = form.save()
				update_session_auth_hash(request, user)
				messages.success(request, 'Your MediaDrive account password has been changed successfully.')
				return redirect('change_password')
			else:
				messages.error(request, 'Getting some error, Please write correct password.')
		else:
			form = ChangePasswordForm(request.user)
			starred_counts = 0
			starred_data = StarredFolderModel.objects.filter(user=request.user)
			starred_files_data = StarredFilesModel.objects.filter(user=request.user)
			starred_files_move_to_folder = StarredFileMoveToFolderModel.objects.filter(user=request.user)
			starred_counts = starred_data.count() + starred_files_data.count() + starred_files_move_to_folder.count()
			context = {'forms':form,'starred_counts':starred_counts}
		return render(request, 'change_password.html',context)
	else:
		return redirect('login')


class UserAccountDeleteClass(TemplateView):
	def post(self, request, phone):
		if request.user.is_authenticated:
			userdata = UsersAccounts.objects.get(phone=phone)
			userdata.delete()
			return redirect('login')
		else:
			return redirect('login')


class LogoutClass(LogoutView):
	next_page = '/authentication/'