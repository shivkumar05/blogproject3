
from django.shortcuts import redirect
from .models import *
from django.contrib import messages

from django.contrib.auth import authenticate,logout,login

from .serializers import *
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes,parser_classes
from rest_framework import generics ,response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser ,JSONParser
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
import uuid
from .helper import send_forget_password_mail
from django.contrib.auth import get_user_model
User = get_user_model()


   
# Register API  with this Api user can Create their Account 

class Register(APIView):

    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login API  with this Api user can log into their Account 
class Login(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=email, password=password)

        if user:
            serializer = self.serializer_class(user)
            login(request, user)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response({'message': "Invalid credentials, try again"}, status=status.HTTP_401_UNAUTHORIZED)
 
# Forget_password Api with this api user can share change password link to their associate mail id by entering thier username
# working fine but made some changes due to multiparser error
'''
@api_view(['POST'])
@parser_classes([JSONParser])
def Forget_password(request):
    if request.method == 'POST':
        email= request.POST.get('email')
        if not CustomUser.objects.filter(email = email).first():
            messages.success(request,'No User found with this username')
            return response.Response(status=status.HTTP_404_NOT_FOUND)

        user_obj=User.objects.get(email=email)
        token= str(uuid.uuid4())
        profile_obj=User.objects.get(username = user_obj)
        profile_obj.forget_password_token= token 
        profile_obj.save()
        send_forget_password_mail(user_obj.email, token )
        messages.success(request,'Reset Password Email has been sent to your Email ID')
        return response.Response(status=status.HTTP_202_ACCEPTED)

    else:
        return response.Response(status=status.HTTP_400_BAD_REQUEST)
'''
# Forget_password Api with this api user can share change password link to their associate mail id by entering thier username

class Forget_password(APIView):
    parser_classes=[JSONParser]
    serializer_class = forget_password_serializer
    def post(self,request):
        #email= request.POST.get('email')
        serializer = self.serializer_class(data=request.data)
        #print(serializer)
        email=serializer.initial_data.get('email')
        print(email)
        if not CustomUser.objects.filter(email = email).first():
            messages.success(request,'No User found with this username')
            return response.Response(status=status.HTTP_404_NOT_FOUND)
                
        user_obj=User.objects.get(email=email)
        token= str(uuid.uuid4())
        profile_obj=User.objects.get(username = user_obj)
        profile_obj.forget_password_token= token 
        profile_obj.save()
        send_forget_password_mail(user_obj.email, token )
        messages.success(request,'Reset Password Email has been sent to your Email ID')
        return response.Response(status=status.HTTP_202_ACCEPTED)

        

#ChangePassword Api with this api user can change their password
@api_view(['POST','GET'])
@parser_classes([FormParser,MultiPartParser,JSONParser])
def ChangePassword(request , token):
    try:
        print('A')
        profile_obj = User.objects.get(forget_password_token = token)
        print(profile_obj)
        users_id = profile_obj.id
        print(users_id)
        if request.method == 'POST':
            print('B')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            # if user_id is  None:
            #     messages.success(request, 'No user id found.')
            #     return redirect(f'/change-password/{token}/')

            if  new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password/{token}/')

            user_obj = CustomUser.objects.get(id = users_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return response.Response(status=status.HTTP_205_RESET_CONTENT)  
        print('D')     
        return response.Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
    return response.Response(status=status.HTTP_400_BAD_REQUEST)

"""class ChangePassword(APIView):
    parser_classes=[JSONParser]
    serializer_class = Reset_password_serializer
    
    def post(self,request,token):
        profile_obj = User.objects.get(forget_password_token = token)
        print(profile_obj)
        users_id = profile_obj.id
        print(users_id)
        serializer = self.serializer_class(data=request.data)
        print(serializer)
        new_password=serializer.initial_data.get('email')
        user_obj = CustomUser.objects.get(id = users_id)
        user_obj.set_password(new_password)
        user_obj.save()
        return response.Response(status=status.HTTP_205_RESET_CONTENT)  
"""


# User_post api with this user can Post their photos or file with description
class User_Post(APIView):
    #authentication_classes =[BasicAuthentication]
    #permission_classes =[IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        file_serializer = User_Post_serializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#view post Api with this we can see different User's posts
class Post_view(generics.ListCreateAPIView):
    #authentication_classes =[BasicAuthentication]
    #permission_classes =[IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    queryset = Post.objects.all()
    serializer_class = User_Post_serializer

@api_view(['GET'])
def Post_view_user(request,pk):
    if request.method=='GET':
        post=Post.objects.get(user=pk)
        serializer=User_Post_serializer(post,many=False)
        return Response(serializer.data)


# User_Social Api with this Api we can Post User's Social Media URL's
class User_Social(generics.ListCreateAPIView):
    #authentication_classes =[BasicAuthentication]
    #permission_classes =[IsAuthenticated]
    queryset = Social.objects.all()
    serializer_class = Social_serializer

#View_User_Social Api with this we can get different User's Social Media URL's
@api_view(['GET'])
def User_Social_view(request):
    if request.method=='GET':
        user=Social.objects.all()
        serializer=Social_serializer(user,many=True)
        return Response(serializer.data)



# User_Social_Update with this APi User can Update their Social Media URL's
@api_view(['POST','GET'])
#@permission_classes((IsAuthenticated, ))
def User_Social_Update(request,pk):
    if request.method == 'GET':
        social = Social.objects.get(user=pk)
        serializer = Social_serializer(social, many = False)
        return Response(serializer.data)
    elif request.method == 'POST':
        social = Social.objects.get(user=pk)
        serializer = Social_serializer(instance=social, data=request.data )

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)



# User_About Api with this Api we can Post User's Social About
class User_About(generics.ListCreateAPIView):
    #authentication_classes =[BasicAuthentication]
    #permission_classes =[IsAuthenticated]
    queryset = About.objects.all()
    serializer_class = About_serializer



#View_User_About Api with this we can get different User's About
@api_view(['GET'])
def User_About_View(request):
    if request.method=='GET':
        user=About.objects.all()
        serializer=About_serializer(user,many=True)
        return Response(serializer.data)


# User_About_Update with this APi User can Update their About
@api_view(['POST','GET'])
#@permission_classes((IsAuthenticated, ))
def User_About_Update(request,pk):
    if request.method == 'GET':
        about = About.objects.get(user=pk)
        serializer = About_serializer(about, many = False)
        return Response(serializer.data)
    elif request.method == 'POST':
        about = About.objects.get(user=pk)
        serializer = About_serializer(instance=about, data=request.data )

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)


# User_Profile_Pic API with this API User can upload their Profile pic and Background Image
class User_Profile_Pic(generics.ListCreateAPIView):
    #authentication_classes =[BasicAuthentication]
    #permission_classes =[IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    queryset = Profile_Pic.objects.all()
    serializer_class = Profile_Pic_serializer



# User_Profile_Pic_Update with this APi User can Update their About
@api_view(['POST','GET'])
#@permission_classes((IsAuthenticated, ))
#@parser_classes([FormParser,MultiPartParser])
def User_Profile_pic_Update(request,pk):
    if request.method == 'GET':
        profile_pic = Profile_Pic.objects.get(user=pk)
        serializer = Profile_Pic_serializer(profile_pic, many = False)
        return Response(serializer.data)
    elif request.method == 'POST':
        profile_pic = Profile_Pic.objects.get(user=pk)
        serializer = Profile_Pic_serializer(instance=profile_pic, data=request.data )

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)

# Like_Post with this API user can like posts of other users
def Like_Post(request,id):
    post = Post.objects.filter(id = id)
    if request.user in post[0].likes.all():
       post[0].likes.remove(request.user)
    else:
        post[0].likes.add(request.user)
    return response.Response(status=status.HTTP_202_ACCEPTED) 


# User_Comment with this API user can comment on other user's post 
class User_Comment(APIView):
    #authentication_classes =[BasicAuthentication]
    #permission_classes =[IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    def get(self,request,*args,**kwargs):
        snippets = Comment.objects.all()
        serializer = Comment_serializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = Comment_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# PostDetail with this API user can see Detailed view of any Post
@api_view(['GET'])
def PostDetail(request, pk):
    if request.method=='GET':
        eachpost = Post.objects.get(id=pk)
        serializer=User_Post_serializer(eachpost)
    return Response(serializer.data)


# Blog viewset with this API user can post their blogs 
class BlogPost(APIView):
    #authentication_classes =[BasicAuthentication]
    #permission_classes =[IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser,JSONParser)
    def post(self , request) :
        serializer = BlogSerializer(data=request.data) 
        if serializer.is_valid():              
            serializer.save()  
            return Response(serializer.data)  
        else:
            return Response(serializer.errors)  
  

# Blog viewset with this API user can edit their blogs 
@api_view(['PUT'])
#@permission_classes((IsAuthenticated, ))
#@parser_classes([FormParser,MultiPartParser])
def Blog_update(request,pk):
    if request.method == 'PUT':
        blog = Blog.objects.get(id=pk)
        serializer = BlogSerializer(instance=blog, data =request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


@api_view(['GET'])
def Blog_view(request):
    if request.method=='GET':
        blog=Blog.objects.filter(is_approved=True)
        serializer=BlogSerializer(blog,many=True)
        return Response(serializer.data)


# Blog viewset with this API user can delete their blogs 
@api_view(['DELETE'])
#@permission_classes((IsAuthenticated, ))
def Blog_delete(request,pk):
        blog = Blog.objects.get(id=pk)
        blog.delete()
        return Response("Blog is successfully delete") 




#https://github.com/CryceTruly/django-rest-api/tree/main/authentication