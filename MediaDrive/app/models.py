from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



class UserBaseManager(BaseUserManager):
	def create_user(self, phone, email, password=None):
		if not phone:
			raise ValueError('Users must have there phone.')
		if not email:
			raise ValueError('Users must have there email.')

		user = self.model(
			phone = phone,
			email=self.normalize_email(email)
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, phone, email, password):
		user = self.create_user(
			phone=phone,
			email = self.normalize_email(email),
			password=password
		)
		user.is_staff = True
		user.is_admin = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class UsersAccounts(AbstractBaseUser):
	image = models.ImageField(upload_to='user_profile/%y')
	first_name = models.CharField(verbose_name='Full Name', max_length=250)
	email = models.EmailField(verbose_name='Email', unique=True)
	phone = models.CharField(verbose_name='Phone',unique=True, max_length=13)
	create_date = models.DateTimeField(verbose_name='Create Date',auto_now=True)
	last_login = models.DateTimeField(verbose_name='Last Login',auto_now_add=True)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	objects = UserBaseManager()

	USERNAME_FIELD = 'phone'
	REQUIRED_FIELDS = ['email']

	def __str__(self):
		return self.first_name

	def has_perm(self, perms, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True



class FolderModel(models.Model):
	user = models.ForeignKey(UsersAccounts, on_delete=models.CASCADE)
	folder_name = models.CharField(verbose_name='Folder Name',max_length=250)
	starred_folder = models.CharField(verbose_name='Starred Folder',max_length=100)
	create_date = models.DateField(verbose_name='Create Date',auto_now_add=True)
	create_time = models.TimeField(verbose_name='Create Time',auto_now_add=True)

	def __str__(self):
		return self.folder_name


class DuplicateFolderModel(models.Model):
	user = models.ForeignKey(UsersAccounts, on_delete=models.CASCADE)
	folders = models.ForeignKey(FolderModel, on_delete=models.CASCADE)
	create_date = models.DateField(verbose_name='Create Date',auto_now_add=True)
	create_time = models.TimeField(verbose_name='Create Time',auto_now_add=True)

	def __str__(self):
		return self.user


class StarredFolderModel(models.Model):
	user = models.ForeignKey(UsersAccounts,on_delete=models.CASCADE)
	folders = models.ForeignKey(FolderModel,on_delete=models.CASCADE)

	def __str__(self):
		return self.user


class FilesModel(models.Model):
	user = models.ForeignKey(UsersAccounts, on_delete=models.CASCADE)
	file = models.FileField(upload_to='file_upload/%y')
	starred_folder = models.CharField(verbose_name='Starred Folder',max_length=100)
	create_date = models.DateField(verbose_name='Create Date',auto_now_add=True)
	create_time = models.TimeField(verbose_name='Create Time',auto_now_add=True)

	def __str__(self):
		return self.user


class DuplicateFilesModel(models.Model):
	user = models.ForeignKey(UsersAccounts, on_delete=models.CASCADE)
	files_id = models.ForeignKey(FilesModel, on_delete=models.CASCADE)
	create_date = models.DateField(verbose_name='Create Date',auto_now_add=True)
	create_time = models.TimeField(verbose_name='Create Time',auto_now_add=True)

	def __str__(self):
		return self.user


class StarredFilesModel(models.Model):
	user = models.ForeignKey(UsersAccounts,on_delete=models.CASCADE)
	files = models.ForeignKey(FilesModel,on_delete=models.CASCADE)

	def __str__(self):
		return self.user


class FilesMoveToFolderModel(models.Model):
	user = models.ForeignKey(UsersAccounts,on_delete=models.CASCADE)
	files = models.ForeignKey(FilesModel,on_delete=models.CASCADE)
	folders = models.ForeignKey(FolderModel,on_delete=models.CASCADE)

	def __str__(self):
		return self.user


class StarredFileMoveToFolderModel(models.Model):
	user = models.ForeignKey(UsersAccounts,on_delete=models.CASCADE)
	files = models.ForeignKey(FilesModel,on_delete=models.CASCADE)
	folders = models.ForeignKey(FolderModel,on_delete=models.CASCADE)

	def __str__(self):
		return self.user