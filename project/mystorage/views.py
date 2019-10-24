from rest_framework import viewsets
from .models import Essay, Album, Files
from .serializers import EssaySerializer , AlbumSerializer, FilesSerializer
#serch를 위한 import
from rest_framework.filters import SearchFilter
# 파일 업로드 에러 수정
from rest_framework.parsers import MultiPartParser, FormParser
# create() 를 오버라이드 하기 위함
from rest_framework.response import Response
from rest_framework import status
#pagination 구현
from .pagination import MyPagination

class PostViewSet(viewsets.ModelViewSet):
    queryset = Essay.objects.all()
    serializer_class = EssaySerializer

    pagination_class = MyPagination # 해당 클래스를 가지면 디폴트 값이 아닌 mypagination에서 정의한 page size가 들어감

    filter_backends = [SearchFilter] # SearchFiler 기반 작성 백엔드 설정
    search_fields = ('title', 'body') # 검색할 필드 지정

    # author_name 을 만들었으니 자동저장을 위해
    def perform_create(self, serializer): # 내가 직접 작성한 user 를 자동으로 저장
        serializer.save(author=self.request.user)

    # 현재 request 를 보낸 유저 == self.request.user
    # 유저 기반 쿼리셋 필터링(로그인시 자기 글만 보이게)
    def get_queryset(self):
        qs =super().get_queryset()
        if self.request.user.is_staff: # request 날린 유저가 staff 인경우
            pass # 필터링 없이 모든 유저의 글을 확인 할 수 있다.
        elif self.request.user.is_authenticated: # request 날린 유저가 인증되었다면.
            qs =qs.filter(author=self.request.user)
            # request 날린 유저가 author 인 것만 필터링한다
        else:
            qs = qs.none()

        return qs

class ImgViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    # author_name 을 만들었으니 자동저장을 위해
    def perform_create(self, serializer):  # 내가 직접 작성한 user 를 자동으로 저장
        serializer.save(author=self.request.user)

    # 현재 request 를 보낸 유저 == self.request.user
    # 유저 기반 쿼리셋 필터링(로그인시 자기 글만 보이게)
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:  # request 날린 유저가 staff 인경우
            pass  # 필터링 없이 모든 유저의 글을 확인 할 수 있다.
        elif self.request.user.is_authenticated:  # request 날린 유저가 인증되었다면.
            qs = qs.filter(author=self.request.user)
            # request 날린 유저가 author 인 것만 필터링한다
        else:
            qs = qs.none()

        return qs

class FileViewSet(viewsets.ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer

    # 파일 업로드시 에러를 잡기 위해
    # parser_classes 지정이 필요
    # create() -> post 요청 오버라이딩 필요
    parser_classes = (MultiPartParser, FormParser) # 다양한 미디어 형식을 수락함

    def post(self, request, *args, **kwargs):
        serializer = FilesSerializer(data=request.data)
        if serializer.is_valid(): #유효성 검사
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # author_name 을 만들었으니 자동저장을 위해
    def perform_create(self, serializer): # 내가 직접 작성한 user 를 자동으로 저장
        serializer.save(author=self.request.user)

    # 현재 request 를 보낸 유저 == self.request.user
    # 유저 기반 쿼리셋 필터링(로그인시 자기 글만 보이게)
    def get_queryset(self):
        qs =super().get_queryset()
        if self.request.user.is_staff: # request 날린 유저가 staff 인경우
            pass # 필터링 없이 모든 유저의 글을 확인 할 수 있다.
        elif self.request.user.is_authenticated: # request 날린 유저가 인증되었다면.
            qs =qs.filter(author=self.request.user)
            # request 날린 유저가 author 인 것만 필터링한다
        else:
            qs = qs.none()

        return qs