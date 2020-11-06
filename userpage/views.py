from django.shortcuts import render , redirect ,HttpResponse, get_object_or_404
from .models import  Post, Profile, Likepost, Following, Comment
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
# Create your views here.
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import CommentForm

def userHome(request):

    user = Following.objects.get(user= request.user)
    followed_user = [i for i in user.followed.all()]
    followed_user.append(request.user)
    posts = Post.objects.filter(user__in = followed_user).order_by('-pk')
    like_dislike = []
    for post in posts:
        like_dislike = Likepost.objects.filter(post = post, user = request.user)
        if like_dislike:
            like_dislike.append(post)

    context = {'posts':posts, 'like_dislike':like_dislike}
    print(like_dislike)
    return render(request , 'userpage/postfeed.html', context)

def userPost(request):
    if request.method == 'POST':
        image = request.FILES.get('post_image')
        captions = request.POST.get('captions')

        user = request.user

        print(captions, user)

        post_obj = Post(user=user, caption=captions, image=image)
        post_obj.save()
        messages.success(request, "Post created successfully")
        return redirect('/userpage')
    else:
        messages.error(request, "Something Went Wrong!")

    return render(request, 'userpage/postfeed.html')

def userProfile(request, pk):
    user = User.objects.filter(pk=pk)

    if user:
        user = user[0]
        profile = Profile.objects.get(user=user)
        about= profile.about
        profile_pic = profile.profile_pic
        posts = getPosts(user)
        is_following = Following.objects.filter(user = request.user, followed = user)
        follow_obj = Following.objects.get(user = user)
        followers = follow_obj.follower.count()
        followings = follow_obj.followed.count()

        context={
            'user': user,
            'about':about, 
            'profile_pic':profile_pic,
            'posts':posts, 
            'connection': is_following,
            'followers':followers ,
            'following':followings,
            }

    return render(request, 'userpage/profile.html', context)

def getPosts(user):
    users_post = Post.objects.filter(user=user)
    post_list = [users_post[i:i+3] for i in range (0, len(users_post), 3)]
    return post_list

def delPost(request, Uid):
    post = Post.objects.filter(pk=Uid)
    post.delete()
    post_path = post[0].image
    post_path.delete()
    return redirect('/userpage')

def userLike(request):
    post_id = request.GET.get("likeId", "")
    post = Post.objects.get(pk=post_id)
    user = request.user
    like = Likepost.objects.filter(post=post,user=user)
    is_liked =  False
    if is_liked:
        Likepost.dislike(post, user)
    else:
        is_liked = True
        Likepost.liked(post, user)

    resp = {'liked':is_liked }
    response = json.dumps(resp)
    return HttpResponse(response, content_type="application/json")

def follow(request, username):
    main_user = request.user
    follow_user = User.objects.get(username = username)

    following = Following.objects.filter(user = main_user, followed = follow_user)
    is_followed = True if following else False

    if is_followed:
        Following.unfollow(main_user, follow_user)
        is_followed = False
    else:
        Following.follow(main_user, follow_user)
        is_followed = True

    resp ={
        "following": is_followed,
    }

    response = json.dumps(resp)
    return HttpResponse(response, content_type="application/json")

class Search_User(ListView):
        model = User
        template_name = "userpage/search.html"
        
        def get_queryset(self):
            username = self.request.GET.get("username", "")
            queryset = User.objects.filter(username__icontains = username)
            return queryset

##class for post detail 


class Post_Detail(DetailView):
    model= Post
    template_name = "userpage/post_detail.html"
    ordering = ['-id']

    

    def get_context_data(self, *args, **kwargs):
        context = super(Post_Detail, self).get_context_data()

        post_stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = post_stuff.total_likes()
        liked = False

        if post_stuff.likes.filter(id = self.request.user.id).exists():
            liked = True
        context["total_likes"] = total_likes
        context["liked"] = liked
        return context

##Another like model as above one is far too complicated

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))#submitting like form 

    liked = False
    if post.likes.filter(id = request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))


##commenting

class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'userpage/post_comment.html'
    ordering = ['-id']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post_id = self.kwargs['pk']



        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk':self.kwargs['pk']})


class Profile_Detail(DetailView):
    model= Profile
    template_name = "userpage/profile.html"
    ordering = ['-id']

    
