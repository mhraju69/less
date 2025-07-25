# airdrop/views.py

import random
import string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Participant
from .serializers import ParticipantSerializer
from django.http import HttpResponse
import csv


def generate_referral_code(length=10):
    characters = string.ascii_uppercase + string.digits  # A-Z + 0-9
    referral_code = "".join(random.choice(characters) for _ in range(length))
    return referral_code

class RegisterView(APIView):
        def post(self, request):
            wallet = request.data.get('wallet')
            pin = request.data.get('pin')
         
            if not wallet or not pin:
                return Response({'message': 'Wallet address and pin are required'}, status=status.HTTP_400_BAD_REQUEST)

            if Participant.objects.filter(wallet=wallet).exists():
                participant = Participant.objects.get(wallet=wallet)
                
                if participant.pin == pin:
                    serializer = ParticipantSerializer(participant)
                    return Response({'data': serializer.data, 'message': 'existing_user'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Incorrect pin'}, status=status.HTTP_400_BAD_REQUEST)


            referred_by = request.data.get('referred_by')
            twitter = request.data.get('twitter')
            retweet = request.data.get('retweet')
            telegram = request.data.get('telegram')            
            referral_code = generate_referral_code()

            participant = Participant.objects.create(wallet=wallet, referred_by=referred_by,twitter=twitter, retweet=retweet, pin=pin,referral_code=referral_code,telegram=telegram, points=4000)
            
            if referred_by:
                try:
                    referrer = Participant.objects.get(referral_code=referred_by)
                    referrer.points += 100  # Add referral bonus
                    referrer.save()
                except:
                    pass
            return Response({'referral_code':referral_code}, status=status.HTTP_201_CREATED)


# airdrop/views.py (continued)


class ExportCSVView(APIView):
    def get(self, request, *args, **kwargs):
        wallet = kwargs.get('wallet') 
        print(f"Received wallet: {wallet}")
        if not wallet:
            return Response({"error": "Wallet parameter is required"}, status=400)
        participants = Participant.objects.filter(wallet=wallet)

        if not participants.exists():
            return Response({"error": "No participant found for this wallet"}, status=404)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="participants.csv"'

        writer = csv.writer(response)
        writer.writerow(['Wallet', 'Points', 'Referral Code', 'Referred By'])
        for p in participants:
            writer.writerow([p.wallet, p.points, p.referral_code, p.referred_by])

        return response
