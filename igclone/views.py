from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Publication, Comment
from .forms import UpdateUserForm, InstagramUserForm, UpdatePublicationForm
from .serializers import PublicationSerializer, SwitchThemeSerializer, CommentSerializer
from .filters import FollowingFilter, FollowerFilter


@login_required(login_url='login_register:login')
@api_view(['GET', 'POST'])
def index(request):
  brad = User.objects.get(id=36)
  print("BRAD: ", brad.id)
  # The logged in user
  user = request.user
  # Get all publications of the logged user
  user_pubs = user.publication_set.all()
  # Get all users whom the logged in user follows to
  following_users = user.instagramuser.following.all()

  # Get all Publications that the logged in user can see
  pub_list = []
  for following_user in following_users:
    pub_list += following_user.publication_set.all()
  pub_list.extend(user_pubs)

  # Sort Publications by created date
  following_pub_list = sorted(pub_list, reverse=True, key=lambda obj: obj.pub_date)

  # Like/Unlike Handler
  if request.is_ajax():
    # if request.POST.get('like') == 'like':
      publication_id = request.POST.get('publication_id')
      publication = Publication.objects.get(id=publication_id)
      if user not in publication.liked.all():
        publication.liked.add(user)
      else:
        publication.liked.remove(user)
      pub_serializer = PublicationSerializer(publication, many=False)
      return JsonResponse({"likes_number":publication.likes, 'user_id':user.id, "pub_liked":pub_serializer.data}, status=200)

  # Suggested list
  all_users = User.objects.all()
  suggestioned_users = []
  for suggestioned_user in all_users:
    if user not in suggestioned_user.instagramuser.follower.all():
      suggestioned_users.append(suggestioned_user)
    else:
      pass

  suggestioned_users.remove(user)
  suggestioned_list = sorted(suggestioned_users, reverse=True, key=lambda obj: obj.instagramuser.followers)

  # 
  # Comment Section
  # 
  
  # check if Fetch API call
  if request.headers.get('content-type') == 'application/json':

    # get 'comment text' from fetch
    comment_text = request.data['comment_text']
    
    # get Publication Id from fetch
    pub_id = request.data['id_publication']

    # Publication
    pub = Publication.objects.get(id=pub_id)
    
    # Author of Comment
    author_name = user.first_name
    
    # check if Comment Text is not empty
    if comment_text != '':
      
      # creating a new comment
      new_comment = Comment.objects.create(publication=pub, author=author_name, body=comment_text)
      # saving a new comment
      new_comment.save()

      # 3 last comments of publication in a reversed order, (the newest on top)
      comments = pub.comments.all().order_by('-date_added')[:3]

      # serializing comments
      comm_serializer = CommentSerializer(comments, many=True)

      return Response(comm_serializer.data)
      
    else:
      pass

  context = {'user':user, 'publications':following_pub_list, 'suggestioned_users':suggestioned_list[:5]}
  return render(request, 'igclone/index.html', context)


@login_required(login_url='login_register:login')
@api_view(['GET'])
def userPage(request, pk):    
  user = User.objects.get(id=pk)
  switch_theme = user.instagramuser.switchtheme

  if request.headers.get('content-type') == 'application/json':
    serializer = SwitchThemeSerializer(switch_theme)
    return Response(serializer.data)

  user_attributes = user.publication_set.order_by('-pub_date').all()
  num_user_photos = user_attributes.count()
  num_followers = user.instagramuser.followers
  num_following = user.instagramuser.followings
  context = {'user':user, 'user_attributes':user_attributes, 'num_user_photos':num_user_photos, 'num_followers':num_followers, 'num_following':num_following}

  return render(request, 'igclone/user_page.html', context)


@login_required(login_url='login_register:login')
def publicationDetail(request, u_pk, p_pk):

  # user = request.user
  post = Publication.objects.get(id=p_pk)
  likes = post.likes
  liked_list = post.liked.all()
  print("LIKE LIST: ", post.liked.all())
  comments = post.comments.all()
  num_comments = post.comments.all().count()
  # context = {'post':post, 'form_post':form_post}
  context = {'post':post, 'likes':likes, 'liked_list':liked_list, 'comments':comments, 'num_comments':num_comments}
  return render(request, 'igclone/publication.html', context)


@login_required(login_url='login_register:login')
def add_photo(request):

  user = request.user

  if request.method == 'POST':
    image = request.FILES.get('pub_img')
    description = request.POST.get('descrip')

    publication = Publication(user=user, image=image, description=description)
    publication.save()

    return redirect('user_page', user.pk)

  return render(request, 'igclone/add_photo.html')


@login_required(login_url='login_register:login')
@api_view(['GET', 'POST'])
def edit_profile(request, pk):

  user = User.objects.get(id=pk)
  instagramuser = user.instagramuser
  form = UpdateUserForm(instance=user)
  profile_pic_form = InstagramUserForm(instance=instagramuser)

  # check if it's an API call. and if it is then swap the theme to the opposite one
  if request.headers.get('content-type') == 'application/json':
    # get user's id that fetch API provides from edit_profile.js
    data = request.data['user']
    # query user
    api_user = User.objects.get(id=data)

    # swaping theme
    if api_user.instagramuser.switchtheme.theme == 'https://timbucketaws.s3.amazonaws.com/static/css/main.css':
      api_user.instagramuser.switchtheme.theme = 'https://timbucketaws.s3.amazonaws.com/static/css/swap_color.css'
      api_user.instagramuser.switchtheme.save()
    else:
      api_user.instagramuser.switchtheme.theme = 'https://timbucketaws.s3.amazonaws.com/static/css/main.css'
      api_user.instagramuser.switchtheme.save()
    theme = api_user.instagramuser.switchtheme

    # serializering a SwitchTheme model
    serializer = SwitchThemeSerializer(theme)
    return Response(serializer.data)

  # Update user's information
  if request.POST.get('update') == 'update':    
    profile_pic_form = InstagramUserForm(request.POST, request.FILES, instance=instagramuser)
    form = UpdateUserForm(request.POST, instance=user)
    if form.is_valid() and profile_pic_form.is_valid():
      form.save() and profile_pic_form.save()
    return redirect('edit_profile', user.id)

  context = {'form':form, 'pic_form':profile_pic_form}

  return render(request, 'igclone/edit_profile.html', context)


@login_required(login_url='login_register:login')
def delete_profile(request, pk):
  user = User.objects.get(id=pk)
  if request.method == 'POST':
    user.delete()
    return redirect('login_register:login')
  context = {'user':user}
  return render(request, 'igclone/delete_profile.html', context)


@login_required(login_url='login_register:login')
def follow_user(request, pk):
  guest_user = request.user
  host_user = User.objects.get(id=pk)
  
  if request.method == 'POST':
    if host_user not in guest_user.instagramuser.following.all():
      guest_user.instagramuser.following.add(host_user)
      host_user.instagramuser.follower.add(guest_user)
    else:
      guest_user.instagramuser.following.remove(host_user)
      host_user.instagramuser.follower.remove(guest_user)
    return redirect('follow_user', host_user.id)

  users_photos = host_user.publication_set.order_by('-pub_date').all()
  num_users_photos = users_photos.count()

  num_followers = host_user.instagramuser.followers
  num_following = host_user.instagramuser.followings

  context = {'host_user':host_user, 'guest_user':guest_user, 'users_photos':users_photos, 'num_users_photos':num_users_photos, 'num_followers':num_followers, 'num_following':num_following}
  return render(request, 'igclone/follow_user.html', context)


@login_required(login_url='login_register:login')
def post_user(request, pk):
  user = request.user
  post = Publication.objects.get(id=pk)
  form_post = UpdatePublicationForm(instance=post)
  if request.method == 'POST':
    form_post = UpdatePublicationForm(request.POST, request.FILES, instance=post)
    if form_post.is_valid:
      form_post.save()
    return redirect('user_page', user.id)
  context = {'post':post, 'form_post':form_post}
  return render(request, 'igclone/post_user.html', context)


@login_required(login_url='login_register:login')
def delete_post(request, pk):
  user = request.user
  post = Publication.objects.get(id=pk)
  if request.method == 'POST':
    post.delete()
    return redirect('user_page', user.id)
  context = {'post':post}
  return render(request, 'igclone/delete_post.html', context)


@login_required(login_url='login_register:login')
def followingPage(request, pk):
  user = request.user
  following_list = user.instagramuser.following.all()
  following_filter = FollowingFilter(request.GET, queryset=following_list)
  following_list = following_filter.qs
  if request.method == 'POST':
    following_id = request.POST.get('following_id')
    following_user = User.objects.get(id=following_id)
    user.instagramuser.following.remove(following_user)
    following_user.instagramuser.follower.remove(user)
    # return redirect('following', user.id)
    return redirect('following')
  context = {'list':following_list, 'following_filter':following_filter}
  return render(request, 'igclone/following.html', context)



@login_required(login_url='login_register:login')
def followersPage(request, pk):
  user = request.user
  follower_list = user.instagramuser.follower.all()
  follower_filter = FollowerFilter(request.GET, queryset=follower_list)
  follower_list = follower_filter.qs
  if request.method == 'POST':
    follower_id = request.POST.get('follower_id')
    follower_user = User.objects.get(id=follower_id)
    if request.POST.get('follow_back') == 'follow_back':
      user.instagramuser.following.add(follower_user)
      follower_user.instagramuser.follower.add(user)
    else:
      user.instagramuser.follower.remove(follower_user)
      follower_user.instagramuser.following.remove(user)
  context = {'list':follower_list, 'follower_filter':follower_filter}
  return render(request, 'igclone/follower.html', context)


@login_required(login_url='login_register:login')
def followingList(request, pk):
  host_user = User.objects.get(id=pk)
  following_list = host_user.instagramuser.following.all()
  following_filter = FollowingFilter(request.GET, queryset=following_list)
  following_list = following_filter.qs
  context = {'list':following_list, 'following_filter':following_filter}
  return render(request, 'igclone/following_list.html', context)


@login_required(login_url='login_register:login')
def followerList(request, pk):
  host_user = User.objects.get(id=pk)
  follower_list = host_user.instagramuser.follower.all()
  follower_filter = FollowerFilter(request.GET, queryset=follower_list)
  follower_list = follower_filter.qs
  context = {'list':follower_list, 'follower_filter':follower_filter}
  return render(request, 'igclone/follower_list.html', context) 