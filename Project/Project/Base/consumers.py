from distutils.cmd import Command
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from asgiref.sync import async_to_sync



class ConferenceRoom(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = "room_%s" % self.room_name

        await (self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.send(text_data= json.dumps({'status': "connected from new async json2 consumer"}))
        print("i am connected ")
        

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        print("i am now disconnected")


    async def receive_json(self, content):

        if(content['command']=='join'):
            await self.channel_layer.group_send(
                self.room_group_name,{
                    'type': 'join.message'
                }
            )

        elif(content['command'] == 'offer'):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'offer.message',
                    'offer': content['offer']
                }
            )

        elif(content['command'] == 'answer'):
            await self.channel_layer.group_send(
                self.room_group_name,{
                    'type': 'answer.message',
                    'answer': content['answer']
                }
            )

        
        elif(content['command']== 'candidate'):
            await self.channel_layer.group_send(
                self.room_group_name,{
                    'type': 'candidate.message',
                    'candidate': content['candidate'],
                    'iscreated': content['iscreated']
                }
            )
        
        
    
    async def join_message(self, event):
        await self.send_json({
            'command': 'join'
        })



    async def offer_message(self, event):
        await self.send_json({
            'command': 'offer',
            'offer': event['offer']
        })

    async def answer_message(self, event):
        await self.send_json({
            'command': 'answer',
            'answer': event['answer']
        })



    async def candidate_message(self, event):
        await self.send_json({
            'command': 'candidate',
            'candidate': event['candidate'],
            'iscreated': event['iscreated']
        })


    async def order_message(self,event):
        # message = json.loads(event['message'])
        await self.send_json({
            'command': 'message',
            'message': event['message'],
        })
        


        # await self.channel_layer.send(
        #     self.room_group_name,{
        #         'type': 'send.sip',
        #         'receive_dict': receive_dict
        #     }

        # )

    
    # async def send_sip(self, event):
    #     receive_dict = event['receive_dict']
    #     await self.send(text_data=json.dumps(receive_dict))