from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import RSVP,WeddingMedia
from .serializers import RSVPSerializer,WeddingMediaSerializer
import cloudinary.uploader

from decouple import config
import cloudinary

cloudinary.config(
    cloud_name=config("CLOUDINARY_CLOUD_NAME"),
    api_key=config("CLOUDINARY_API_KEY"),
    api_secret=config("CLOUDINARY_API_SECRET")
)


@api_view(['POST'])
def submit_rsvp(request):
    serializer = RSVPSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "RSVP submitted successfully", "data": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def vip_details(request, token):
    try:
        vip = RSVP.objects.get(vip_token=token, is_vip=True)
    except RSVP.DoesNotExist:
        return Response({"error": "Invalid VIP link"}, status=404)

    serializer = RSVPSerializer(vip)
    return Response(serializer.data)


@api_view(['POST'])
def vip_confirm(request, token):
    try:
        vip = RSVP.objects.get(vip_token=token, is_vip=True)
    except RSVP.DoesNotExist:
        return Response({"error": "Invalid VIP link"}, status=404)

    vip.attendance = 'yes'
    vip.save()

    return Response({"message": "VIP attendance confirmed"})



@api_view(['POST'])
def upload_media(request):
    file = request.FILES.get('file')

    if not file:
        return Response({"error": "rsvp and file are required"}, status=400)

    # Upload to Cloudinary
    upload_result = cloudinary.uploader.upload(
        file,
        resource_type="auto"   # handles both video & image
    )

    media_type = "video" if upload_result.get("resource_type") == "video" else "image"

    media = WeddingMedia.objects.create(
        media_type=media_type,
        media_url=upload_result["secure_url"]
    )

    serializer = WeddingMediaSerializer(media)
    return Response(serializer.data)



@api_view(['GET'])
def list_media(request):
    media = WeddingMedia.objects.all().order_by('-created_at')
    serializer = WeddingMediaSerializer(media, many=True)
    return Response(serializer.data)

