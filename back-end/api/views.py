from rest_framework.response import Response
from rest_framework import status
from .models import *

from rest_framework.decorators import api_view, authentication_classes
import argon2
from rest_framework_simplejwt.tokens import RefreshToken
import whisper
from summariser.views import summaryFunction
from statement.views import generate_statement
import zipfile
import os
from django.http import FileResponse



ph = argon2.PasswordHasher()
model = whisper.load_model("base")

# Create your views here.
@api_view(['POST'])
@authentication_classes([])
def createAccount(request):
    user_fname = request.data['fname'].strip()
    user_lname = request.data['lname'].strip()
    user_email = request.data['email'].strip()
    user_password = request.data['password'].strip()
    
    hash = ph.hash(user_password)

    try:
        userExist = Users.objects.get(email=user_email)
        return Response(status=409)
    except:
        userObj = Users(first_name=user_fname, last_name=user_lname, email=user_email, password=hash)
        userObj.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def deleteAccount(request):
    user = request.user.id
    refresh_token = request.COOKIES.get("refresh_token")
    if refresh_token:
        try:
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()
        except Exception as e:
            return Response({"error": "problem invalidating token: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


    try:
        userObj = Users.objects.get(id = user)
        userObj.delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@authentication_classes([])
def resetPassword(request):
    user_email = request.data['email']
    current_password = request.data['password']
    new_password = request.data['new_password']

    try:
        userObj = Users.objects.get(email = user_email)

        verify = ph.verify(userObj, current_password)
        if not verify:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        hash = ph.hash(new_password)
        userObj.password = hash
        userObj.save()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
def updateAccountDetails(request):
    user = request.user.id
    email = request.data['email']
    current_password = request.data['current_password']
    new_password = request.data['new_password']
    
    print('password',current_password)

    try:
        userObj = Users.objects.get(id = user)
        print('here')
        if email != '':
            userObj.email = email
            print('email')
        
        if current_password != '':
            try:
                ph.verify(userObj.password, current_password)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            hash = ph.hash(new_password)
            userObj.password = hash
        
        userObj.save()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  

@api_view(['POST'])
@authentication_classes([])
def loginUser(request):
    user_email = request.data['email'].strip()
    user_password = request.data['password'].strip()

    try:
        userObj = Users.objects.get(email=user_email)
        ph.verify(userObj.password, user_password)
        refresh = RefreshToken.for_user(userObj)
        response = Response(status=status.HTTP_200_OK)
        response.set_cookie(key="api_token", value = str(refresh.access_token), samesite=None, secure=True)
        response.set_cookie(key="refresh_token", value = str(refresh), httponly=True, samesite=None, secure=True)

        return response
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logoutUser(request):
    refresh_token = request.COOKIES.get("refresh_token")

    if refresh_token:
        try:
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()
        except Exception as e:
            return Response({"error": "problem invalidating token: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)    
        
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def getAccountSettings(request):
    user = request.user.id

    try:
        userObj = Users.objects.get(id = user)
        userData = {
            'first_name': userObj.first_name,
            'last_name': userObj.last_name,
            'email': userObj.email,
        }

        return Response({'user': userData}, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def createSession(request):
    session_Name = request.data['session_name'].strip()
    user = request.user.id
    sessionObj = Sessions(user_id_id=user, session_name=session_Name)
    try:
        checkSessionExist = Sessions.objects.get(user_id_id=user, session_name=session_Name) 
        return Response({'Error': 'Session name is not unique'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        sessionObj.save()
        session_id = sessionObj.id
        client_fname = request.data['fname'].strip()
        client_lname = request.data['lname'].strip()
        client_email = request.data['email'].strip
        clientObj = Interviewees(first_name=client_fname, last_name=client_lname, session_id_id=session_id, email=client_email)
        clientObj.save()
        return Response(status=status.HTTP_200_OK)



@api_view(['POST'])
def deleteSession(request):
    user = request.user.id
    session_id = request.data['session_id']
   
    try:
        sessionObj = Sessions.objects.get(user_id_id=user, id=session_id)
        sessionObj.delete()
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    return Response(status=status.HTTP_200_OK)



@api_view(['GET'])
def getSessionList(request):
    user = request.user.id
    sessionList = Sessions.objects.filter(user_id_id=user).values('id','session_name', 'transcription', 'summary')
    return Response({'data': sessionList}, status=status.HTTP_200_OK)



@api_view(['POST'])
def getSummary(request):
    user = request.user.id
    session_id = request.data['session_id']

    try:
        sessionObj = Sessions.objects.get(id=session_id, user_id_id=user)
        print('here')
        transcription = sessionObj.transcription.strip()
        text = summaryFunction(transcription)
        if text is None: # if no transcription, it will stop execution
            return Response(status=500)
        sessionObj.summary = text
        sessionObj.save()
        return Response({'summary': text}, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
def test(request):
    user = request.user.id
    sessionID = 1

    try:
        x = Sessions.objects.get(id = sessionID, user_id_id = user)
        x.transcription = '''Okay, so just need to confirm the spelling of your name. I've got S-K-Y-E as the first
name. And then I've got the surname W-H-I-T-E-L-E-Y. Okay, do you have any middle names? Marie.
And how do I spell that? M-A-R-W-E. Okay. And I've got your date of birth here as 2nd
of September 1987, is that correct? That's correct. Okay. All right. And just confirming
that I'm providing this statement in relation to a claim for workers' compensation for
injuries sustained in the course of my employment with J-K-R. Yes. Okay. So just to let you know,
I'm going to be referring to the company you work for J-K-R as the insured for this, the
entirety of this statement, because it has the policy that the claim is being made under.
What's the address of J-K-R's office? Number 4 Fleet Street, sorry, number 5 Fleet Street,
North Parramatta. I think it's 2152. Okay. And did your injury occur at that address?
Yes, it did. Okay. All right. And what's your current residential address? Number 5 Smith
Street, Parramatta, 2150. Okay. And what's your marital status? Single. Okay. Do you have
any dependent children? No. Just a cat. Oh, that's cute. How old is your cat? She's very
old, she's 18. Her name's Myrtle. Very nice. Very nice. Okay. And who, apart from Myrtle,
who resides with you at that address? Just Myrtle. Okay. All right. I understand we're
talking about injuries your lower back today. Yes, that's right. Okay. Have you ever suffered prior
to this incident? Have you ever suffered from any previous injury or any previous issues
with your back? No. I have had some neck problems, but not back problems. Okay. Have you ever
made a previous claim for workers' compensation? Not at this job. Okay. But you have previously
suffered? No. Not at any job. Sorry. Okay. Okay. Do you suffer from any medical conditions,
sort of serious enough that you need to be on prescription medication, or see a doctor
regularly to kind of start on top of them? No. Sometimes I take medication for my neck
pain, but that's all. Okay. Is that prescription medication? No. All right. Since you've worked
at this job, have you ever had a second job or alternate employment? While I'm working at
this current job? Yeah. No. So that means you've never had two jobs at once, another job aside
from this one? No, I haven't. All right. What do you enjoy doing outside of work in terms of sports,
hobbies, activities, interests? I like to paint, cooking, I walk, I go bushwalking. That's about it.
Okay. And have you ever been injured in a non-work accident? That's an accident anywhere
outside the workplace, such as at home, at the gym, a car accident, anything like that? I was hit
by a car when I was very young. Okay. I was maybe 15 or 16. Yep. Okay. What body parts did you injure?
My right leg. And what type of injury broke any bones? I had a hematoma and a hairline fracture in
my femur. Hematoma. I'm going to spell that. I'm going to spell it for you. Go for it. H-A-E-M-A-T-O-M-A.
Thank you. And that was in your right leg? Yes. Okay. And a hairline fracture of my right thigh bone?
Okay. And what treatment did you have for those injuries? I remember going to the hospital and
needing to put a brace on my leg. And I think the bone must have healed itself. I don't really
remember needing any other treatment after that. I still have the hematoma in my leg though.
Okay. Would you consider your right leg when you suffered this injury to have otherwise been fine
and 100% at the time of this injury? Yeah. There was no, I didn't have any other problems with it.
Okay. Any other non-work injuries you've ever suffered? I did trip over a mat at an airport once
and landed on my right knee. About how long ago was that? I would have been maybe seven years ago.
So about 2018? Yeah. Okay. And you fell on your right knee? Yes. And what injury did you suffer then?
I never actually got it looked at. It was just so I have like a piece of bone floating around in my
knee. Yep. But I've never actually had it x-rayed or looked at. It's just sort of swells up every now
and then. Okay. And you said you haven't received any scans or treatments for that? No. How do you know
there's a piece of bone floating if you haven't had a scan? Because I can feel it when I touch it with my
hand. Do you want to feel? It wouldn't be very professional. Oh, okay. Sorry. I'm not qualified.
Okay. And does that condition to your right knee? Does that affect your work at all? Do you have to do any
modified or restricted tasks? No. It only affects if I'm like exercising and I'm having to kneel on my knees.
Okay. No worries. All right. Prior to your employment with JKR, just tell me a little bit about your work history.
I was a nurse for 10 years, but it was cosmetic nursing in a private clinic. So I was a cosmetic
injector. Sorry, that's my rice cooker. Go for it, please.
Okay. Sorry. Very good. Okay. So you're a cosmetic nurse and then you went straight into this job?
Yes. Okay. All right. And did that job as a cosmetic nurse that involved much manual handling or heavy
lifting? No. It was all in a private clinic. Think of it more as like beauty therapy type
sort of movements and things like that.
Okay. All right. And what professional qualifications or trades do you have?
I have a diploma of nursing. Yep. I have a set foreign leadership and management.
I have a set foreign business and I'm currently studying.
Okay. Before you started this job, did they have you do a pre-employment medical examination or
did you have to fill out a medical declaration? No. So I did the business I work for now,
I've moved into like I've worked for different RTOs before this one. I don't know if that is relevant.
Oh, so that was a different employer? Yes. Okay. Yeah, I'll have to go back.
Okay. So that's your previous employment? Yeah. So how long did you work for a different
employer? It would have been five years or about. And what was the name of that?
That was National Training Organization.
National Training Organization? Yes. Very outlandish name.
National for about five years? Yes.
Okay. And did that job involve much manual handling or heavy lifting? No.
Okay. All right. About when did you come into employment with the insured?
So it would have been
2022. 2022? Yes. Can you remember about what time it in? Oh, I could. Maybe
April, I think. April or May.
Okay. What was your role when you commenced? Training Coordinator.
And were you employed full-time, part-time or casual? Full-time.
And where were you based at that time when you commenced employment?
We were working out of my boss's house in Oakland's.
Okay. And about when did you move to the current location?
About a year. And it was in November the following year. So about a year and three or four months.
So you moved about November 2023? Yes.
Okay. And has there been any change to your role since? Yes. Okay. What was that?
I was promoted to Training Manager. And about when was that?
It was a year ago now. So about March 2024? Yes. And that's your current role? Yes.
Okay. All right. What are your just general hours and days at your work?
Um, eight till four, Monday to Friday. Does vary a little bit, but that's generally what I do.
Do you ever do any overtime? Um, unpaid overtime?
Yeah, it counts. Yeah. Approximately how many hours a week are you overtime?
Oh, maybe one. It's more working outside my nominal hours rather than extra hours.
Okay.
All right. And um,
do you, are you entitled to a break? And if so, um, what, how long is your break?
My break is half an hour of unpaid lunch break.
And you always get to take your break? Yes.
Okay. All right. Um, think about when you first started with this company,
did you receive an induction and initial training that included material on safe
manual handling or lifting technique? Not that I can remember. No.
Did you receive an induction and initial training just generally?
Uh, no, because moving to my, this current job was my manager was my manager of the previous job.
So she already knew that I could do the role. Um, it was just moving into her newly opened company.
What's the name of this person? Penny. That's her name?
I think it's limb. Okay.
L. I. M. Yes. Okay.
And she's now owner of the company? Yes.
And then you worked with her at the previous employment and national training organization?
Yes, I did.
Okay.
And how, approximately how long did, how long had you previously worked together for?
Um, so I can't remember whatever the year was. I think it was 2019 or 2018 that I started at
national training organization. Yep. She was the operations manager at the time. So about
three or four years? Yes. Uh, more than that. It was about five years. About five years?
It was a 2018. I think it was that I started working there.
Okay. Um, since you've started working for this company in 2022, have you ever received any
further training or refresher training that's addressed manual handling or safe lifting technique?
No, definitely not.
All right. And do you know if the insured has any policies or procedures in place? Now this could
be, it's pretty broad. It can include like a employee handbook, actual written policies and
procedures that might be kept in the office or even signage on the walls that address safe
lifting technique or manual handling. No, the only thing that I know of that holds anything like that
is actual training materials that we use for students, but not staff related policies or
procedures. So you're a training organization, but you don't have the procedures. Exactly right.
So we're training other people how to do it, but we don't have our own policies or procedures.
Okay, no worries. All right. On an average day of work, how many people do you generally work
alongside? Three. And that's through other people apart from you? Yes. But my boss is currently on
maternity leave, so she hasn't been there for almost 10 months. Okay. So maybe in the last 10
months, it's mostly been two people.
And who are the other two people? One is Stephanie and one is Wendy.
What's, do you know their surnames? Stephanie's surname is Lee.
L-W-E? I think so. Okay. And what's her role? She's administration.
And the other one, Wendy? Wendy is, yes, Wendy's operations. I don't know her last name.
Okay.
All right. Are you generally, and who is your supervisor or manager? Is that Miss Lim?
Well, it was, she hired Wendy while she's been on maternity leave, so but never really said that
she was my manager, but I assume she is now my manager.
Okay.
Okay. All right. And when you do your duties, are you generally closely supervised? Like,
are you sort of regularly told what tasks to do or do you work fairly autonomously?
I work autonomously.
All right.
Is there, do you have to, do you have to wear any particular clothing or PPE at work?
No. Only if I'm out on site with employers, I have to wear hybis.
Okay. And is there any mechanical assistance available to you to move objects from place to
place? So things like trolleys, pallet jacks, stuff like that? There's one small trolley.
It's like one of those fold up trolleys that we use to get stuff out of the car and bring
into the office because the parking is not close by.
So it's one of those stand-up trolleys? Yeah, like it folds out into a stand-up trolley.
That's right.
Okay. And if there's a task that, like a manual handling task that you're not confident
in being able to perform alone, is there always someone you can ask assistance from?
No, I wouldn't say always, no.
Sometimes I'm in the office by myself.
Okay. All right. Just explain to me your duties, like an average day of work, what are the main
things you do? I liaise with clients, either via phone or email. I speak to our trainers via phone
or email, allocating training, doing a lot of paperwork,
doing filing type duties. It's mostly admin-based
sitting in front of my computer.
Okay. Have you ever made any complaints or raised any concern about any of your duties?
This could be pretty broad. Your pay, your hours, your duties, work health and safety
issues, personality issues? Yes. Okay. So I did about a year ago when I was promoted,
that promotion didn't come with a change in my pay rate. And I went to my manager after about a month
and voiced my concerns with that. Yep. And it went back and forth for
a couple of months. She then agreed to a pay rise to reflect my promotion.
And were you satisfied with the pay rise? Yes.
I also voiced concerns about a staff member that I felt wasn't pulling their weight.
About when was that? That was just before she went on maternity leave, which was in May last year.
So yeah, May 2024. I don't remember the day.
You complained to Miss Lim? Yes. And who was that about? That was about Stephanie. That's Miss Lee?
Yes. Okay. And what were your concerns that she just wasn't pulling her weight?
Yeah, the workload was building up and I was having to put my things aside to
assist constantly, which was affecting the workflow and the business operations.
And what did Miss Lim do in response to that? She said she spoke to her,
but it's been an ongoing issue since then.
Okay. And has the insured ever had any concerns with your performance or behaviour in the workplace
that they've spoken to you about? Not that I'm aware of, not that I've been told.
I think nothing comes that fearless. I'm sure everyone does.
All right. Let's talk about your injury. I have here on the paperwork that occurred on
February the 7th. Yes, that's right. I think so. Okay. About what time?
It was before lunch, so maybe like 10 o'clock.
Okay. All right. And what time did your arrival work that day? Eight o'clock in the morning.
Okay. Had you consumed any alcohol, drugs or prescription medication in the 24 hours prior
to the injury? No, I don't think so.
Okay. How are you feeling at the time when you started work? Were you feeling fit and well,
or were you feeling a little under the weather, sick or off in any way?
No, I was feeling normal. I don't remember there being any issues that morning.
All right. Tell me what you were doing between when you started your shift at 8am and when the
injury occurred. What did you start your shift off doing? I would have just been at my desk
looking at emails, and I always check my emails when I come in in the morning.
Yeah. I wouldn't have been doing anything out of the ordinary, just processing or
working at my computer.
Was anyone else in the office that morning when you got there?
No, I was by myself.
Okay. All right. What task were you doing or attempting to do when your injury occurred?
I was attempting to pick up a box of paperwork from the floor. I'm putting it on my desk to start sorting.
Okay. Tell me about the dimensions of the box and approximately how heavy you estimate it would
have been. So it's one of those like A4 paper boxes that holds like, I think it's four or five rings
of paper in it. I honestly wouldn't even know what the weight would be, maybe
what's a ring of paper, those, you know, those boxes that you buy, the the paper in bulk
for office works. Yeah, that's right. It was one of those. Okay. And with the amount of paper in it,
it was a four paper? Yes. So would it have weighed similar to if I were to buy one of
those boxes? Yes, exactly. So it's not that light? No.
I have actually requested that those boxes not be put on the floor for this exact reason.
All right, I'll get to that.
Okay. And what and what happens next? So I picked it up to put it up on my desk and I felt
twinge in my lower back very sudden and kind of felt like nerve pain
when shooting down my leg.
And it affected my movement. I was in a lot of pain. Which leg did it go down? The left leg.
Okay. Do you know who left the box on the floor? Yes, it was Stephanie. How do you know that?
Because I saw her put it there. When did you see that? The Friday before.
Because she goes to King's Grove on Thursdays and brings the boxes back with her on the Friday.
So she goes somewhere off site? Yes. It's another office that we work out of.
Okay.
How many boxes will she bring back? Between one and two.
It varies every time she goes there.
Okay. And you mentioned before that you'd raised your concern about Miss Lee doing this.
Yes. So she tends to come in with the boxes and put them on the floor and probably twice I've
said to her, don't put the boxes on the floor because then they need to be picked up and put on
the desk for processing, which is a WHS risk. But she continues to put the boxes on the floor.
Has anyone witnessed you request Miss Lee to stop putting the boxes on the floor?
Toby might have heard me say it. Sorry, I forgot to mention Toby previously. She comes in maybe
once a week just to help with admin tasks. She might have witnessed it at one point.
How do I spell Toby? T-O-B-Y. Okay. You know Toby Serno? Lim. She's Penny's auntie.
Okay. And have you ever complained to Miss Lee about the safety risk of the boxes being left on
the floor? Not Miss Lee, Miss Lim. So Penny Lim. I don't think so.
I think it's only really been an issue since Penny has been on maternity leave. So
I don't see her very regularly and I haven't, haven't brought it up with her.
Okay. What about Wendy? No, I haven't said anything to Wendy.
Okay. Have you, was this the first time you picked up one of the boxes and put it on the
desk or had you previously been doing this? I've previously been doing it,
which was why I requested that it not be put on the floor anymore.
And why was that? How difficult did you find the task?
Because it's quite heavy and I was concerned that someone would injure themselves picking it up and
putting it up on the desk.
I know I have to really brace myself to do it. So
Did you by chance raise your concerns with Miss Lee by email or in writing text or anything like
that or was it verbal? No, it was verbal.
All right.
Tell me about the technique you use to lift the box.
I always bend with my knees and try not to use my back to lift.
I try to use my core. I do some pilates you see. So I know how to use my core to lift.
Right. Very impressive. Very impressive. I thought so too, yeah.
You try to use your core. Yes. And bent, so bent knees and the straight back.
Yes. I also make sure I don't twist when I'm, while I'm lifting.
So as I get in the training.
Well, I do the best I can, but you know, obviously some of these tasks are still
a bit of a hazard in the workplace, especially when you haven't received, you know,
instructions from your boss. Okay. So you said you're, you said you're in a lot of pain afterwards.
What did you do next? I stopped because I couldn't move. I waited for it to sort of
the shooting pain to stop. I tried to sit down, which again was more painful. And then I took some
pain at all. And did you continue working that day?
Yes, I did. I tried to push through the pain. And then when I finished at 4pm, I called my manager
Penny and told her that I had hurt my back.
And that I didn't know if I would be in tomorrow that was still just as painful.
Why didn't you ring her earlier to report it when it happened in the morning?
I was under a lot of pressure with some work tasks that I needed to get done.
I have a lot of training locked in that week. And I knew if I didn't do it, nobody else was
going to. So there was a lot of weight on my shoulders to get that done that day.
I also am hesitant to contact her while she's on maternity leave because I know she's busy with
her baby.
Okay. And you called her so you've told her verbally and you texted her or emailed her?
No, I called her. Okay. And did you tell her how the injury occurred?
Yeah, she asked me and I told her that I was picking up a box.
Okay. And what was Miss Lim's response?
She told me to rest up and to give her an update tomorrow morning on how I was feeling.
And that if I was still in pain and wasn't coming into work that I needed to drive to
the doctors and get a medical certificate. But I didn't drive because I couldn't because I was in too
much pain. So did you drive to work that day? The day the injury happened? Did I drive to work?
Yeah. Yes. So how did you get home? My partner came and picked me up.
He walked there and we drove home.
Okay. And how did you feel the following morning? I was still in a lot of pain.
Okay. And what did you do? I had to call my doctor and do a phone call consult to get a medical
certificate. Okay. Who was your doctor? I'd have to find the certificate. It wasn't my usual doctor.
Okay. And what medical center? It's one in Paramental Westfield.
Okay. How come you didn't go to your regular GP or medical center? They weren't available.
Okay. And what did the doctor prescribe or what did the doctor suggest? They suggested rest with
some light walking. And they suggested panadol because they weren't allowed to give me anything
stronger because of their policy apparently. Okay. Did I send you for any scans?
Yes. I had an ultrasound. You received a referral for an ultrasound? Yes. Right.
Okay. And did they give you a medical certificate? Yes. And how long did the
ELF work? Did the medical certificate give you? I think it was two days.
Okay. And when did you have the ultrasound? On the next day.
So that would have been the 7th of February. It didn't happen on the 5th. You go to the doctor on
the 6th and the next day is the 7th. So I had the ultrasound on the 6th.
I see you had the ultrasound on the same day as you saw the doctor, as you spoke to the doctor
on the phone? Yes. Yes, I did. Sorry. And when did you become aware of the results of the ultrasound?
I think it was like three or four days later when I had a follow-up call with the GT.
And what did the show? I think she said it didn't really show too much.
And they needed to do further investigations with the CT.
And you had your follow-up appointment with the same clinic at Parramatta Woodsville?
Yes. And was it the same doctor you saw previously? Yes.
And you were referred for a CT? Yes.
And you were referred for anything else, any physio or anything else?
Yeah, I did get a referral for a physio as well.
Okay. When did you have the CT? I had it that same day.
And when did you become aware of the results of the CT? My GP called me the same day that I had it.
And what were you informed of? They said I had a bulging disc in my back
and it was putting pressure on my sciatic nerve.
Okay. And all right. And when did you first go for physiotherapy?
I think it was maybe two or three days later. I can't remember exactly.
So within a week? Yes.
And where did you go for physiotherapy? They're on Crown Street in Parramatta.
Do you know the name? I can't remember. Do you know the name of the actual practitioner?
His name is Joe.
It's very expensive. Just so you know.
But you didn't get a plan? I did, but it's still very expensive.
All right. So the epic use, I suppose your claim hasn't been approved yet.
That's correct. And you're having to flip the bill for the moment.
Okay. And you don't know Joe's surname? Yes, Joe Baker.
How many physio sessions have you been to so far?
I go twice a week and I've gone twice a week consistently since the injury.
Okay. And any other treatment? No, only the physio.
Okay. Have you returned to work? Yes, she has me on like duties, but my role is basically the
same as it was. When did you return to work? I think I ended up having about two weeks
off. Yep. And then went back on the Monday, almost two weeks after.
Okay. And when did you make the claim? That week. The same week as you suffered the injury or the
When I returned.
Did you return? Did you make the claim through the Doctor of Parameter Westfields?
Yes. So the same doctor that you'd been seeing the whole way through?
That's right. But you don't know the name?
No, I can find it and send it to you.
I think his first name was Raj, but I'm not 100% sure.
Okay. When did you first tell this doctor that how the injury happened?
It was after the CT scan. I asked him, what do I do about putting in a workers' compensation
thing because it happened at work. But in your first consultation,
you didn't tell him how the injury happened? No. I just said, I picked up a box.
I didn't realise I had to tell him that happened at work for it to be.
I thought it was something I had to speak to my manager about, not the doctor.
Okay. All right. And what was the response? So you waited around two weeks.
Why didn't you make the claim straight away?
As I wasn't 100% sure of the whole process and I couldn't get in touch with my manager since
she's been on maternity leave, sometimes she's difficult to get in touch with.
So you wanted to speak to her about it first? Yes.
So did you end up speaking to her about it before you made the claim?
Yes, but just that day. Okay. So did the day prior to you going to the doctor to make the claim,
you spoke to her? Yes.
And what was her reaction when you told her you were going to make a claim?
She was fine with it. I think she was a little bit surprised that I was still
in pain and having problems. I think she expected me to be better by then.
So when you returned to work, you hadn't made the claim yet. So there was nothing formal
about your capacity like there was no certificate to say what things you could and couldn't do.
So how were the arrangements made for you to go on like duties when you returned?
So I told her that I was still in pain and she basically just said to
not be lifting anything or moving anything around the office.
Yeah, basically to stay away from anything where I might be,
moving any boxes or any paperwork
or anything strenuous, moving boxes from the car to the office, nothing like that.
All right, but otherwise, all your duties and hours were the same? Yes.
Okay, and was there anything,
was there, and when you got your certificate, were there any further restrictions that your
certificate suggested that your doctor suggested that you have?
No, I don't think so. Did your doctor suggest reduced hours or any more modified duties? No.
He just told me to call and make another appointment if my pain got worse.
Okay, and currently are you still working under those restrictions? Yes.
I have had to have a day off here and there because of the pain, but
other than that, I'm doing my normal duties without the lifting or moving paperwork.
Approximately how many days off would you say you've had?
Maybe like five.
Right, okay. And there's been no change in your restrictions or capacity even because of that?
No. But I have no leave left, so I'm taking leave without pay.
Until the claim is approved. I hope maybe you might get that paid back.
Hopefully.
Okay, all right. How is your pain currently? Keep in mind you've had the sessions with the
physio and you're no longer sort of lifting heavy items. I still have the pain every day.
It's not as bad, but it does restrict things that I do as just everyday tasks in my life,
like put my shoes on and bending over in the shower and things like that.
Okay.
Okay. What about at work? How does it feel at work?
Constant pain. What things tend to make it worse or?
Movement. Even just sitting still for long periods of time. When I get up out of my chair,
when I sit down in my chair, or just when I'm not doing anything at all.
What about standing up? When I'm standing still? Yeah. Yeah, I can still feel it.
Is standing worse than sitting or both the same?
It depends if I'm standing for a long period. It's probably the same as sitting for a long period.
Okay. All right. Okay, and what things in your outside life is it affecting things that you
used to be able to do? Is it cooking, painting, bush walking? Is it affecting those things?
Household chores, driving, things like that. Yeah, everything in my everyday life.
Can you elaborate a little bit? So, you know, standing in the kitchen or moving around the
kitchen, bending into my cupboards, anything that involves any type of twisting or bending over.
As I said, putting my shoes on, I haven't been able to go for a bush walk since it happened.
Yeah, it's just even my just everyday walking has been affected.
How are you getting to work now?
I've been catching the tram because I can't walk as far anymore.
Okay. Are you still able to, are there some tasks you can't do at all?
The lifting, anything where I'm lifting anything more than maybe a few kilos.
So, shopping? Yeah.
And who is helping you with things you can no longer do? My partner.
Okay, final question. Sometimes when people make these claims, they're going to have things going
on in their private life that can be relevant. They're usually like sources of stress that
are going on in their private life. I'll give you some generic examples. There can be addiction
issues with drugs, alcohol or gambling, financial problems, relationship or domestic problems,
or maybe concern over the well-being of a loved one, maybe a family member is sick and you're
having to look after them, or even someone you love having recently passed away. They're just
generic examples. Are there any issues in your private life that are stressful that might be
relevant to you having made this claim? No, I don't believe so. My job is stressful,
but it's no more stressful now than it has been for the last five years.
Okay. All right. And sorry, I forgot to ask you before. Do you know if you did mislead,
make an incident report of this, or did she have you make an incident report?
I didn't make one. I don't know. She didn't request me to.
Okay. And do you have any text messages or anything in writing in which you refer to the
incident, preferably closer to the day of the incident, if not on the day? And this can be
text to anyone, your partner, friends, family. Yeah, I texted my partner because he had to come
and get me from work and told him that I'd hurt my back.
And can I just have a look at that text, would you be able to bring it up?
Yeah, sure. Okay. Yeah. Okay. And that's good. That's good. You do say that you were lifting
a box today in the office. Okay. Would you mind screenshotting that and sending it to me, please?
Yeah, no problem.
Okay. Excellent. All right. Very good. I'll send you a copy of this by email.
For you to review. And if you can sign it and have it witnessed and send it back to me, that'd be
great. Okay. Thank you. Thank you. Bye.
'''
        x.save()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # try:
    #     x = AudioRecordings.objects.all()
    #     for y in x:
    #         print(y.audio_path)
    #     return Response(status=status.HTTP_200_OK)
    # except:
    #     return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def generateStatement(request):
    user = request.user.id
    sessionID = request.data['session_id']
    try:
        clientObj = Interviewees.objects.get(session_id=sessionID)
        sessionObj = Sessions.objects.get(id=sessionID, user_id_id=user)
        templateObj = StatementTemplates.objects.get(id = 1)

        transcription = sessionObj.transcription.strip()
        text = generate_statement(transcription, templateObj.template_path.path)
        if text is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        statement = Statements(user_id_id=user, interviewee_id_id=clientObj.id, statement_content=text)
        statement.save()
        return Response({'statement_id': statement.id}, status=status.HTTP_200_OK)
        
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['POST'])
def getStatement(request):
    user = request.user.id
    statement_id = request.data['statement_id']
    try:
        statementObj = Statements.objects.get(id = statement_id, user_id_id = user)
        content = statementObj.statement_content
        return Response({'statement': content}, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET'])
def getStatementList(request):
    user = request.user.id

    try:
        statementObj = Statements.objects.filter(user_id_id = user)
        clientList = []
        for obj in statementObj:
            client = Interviewees.objects.get(id = obj.interviewee_id_id)
            dict = {
                'statement_id': obj.id,
                'client_first_name': client.first_name,
                'client_last_name': client.last_name,
                'statement_content': obj.statement_content,
            }
            clientList.append(dict)
        return Response({'list': clientList},status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def updateStatement(request):
    user = request.user.id
    statement_id = request.data['statement_id']
    updated_statement = request.data['updated_statement']

    try:
        statementObj = Statements.objects.get(id = statement_id, user_id_id = user)
        statementObj.statement_content = updated_statement
        statementObj.save()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
def deleteStatement(request):
    user = request.user.id
    statement_id = request.data['statement_id']

    try:
        statementObj = Statements.objects.get(id = statement_id, user_id_id = user)
        statementObj.delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def uploadRecordings(request):
    sessionID = request.data['session_id']
    name = request.data['audio_name']
    fullRecording = request.FILES['fullRecording']

    audioObj = AudioRecordings(session_id_id = sessionID, audio_name = name, audio_path = fullRecording)
    audioObj.save()

    print(audioObj.audio_path)
    
    return Response(status=status.HTTP_200_OK)

# WORKING BUT DISABLED FOR NOW
# @api_view(['POST'])
# def downloadRecording(request):
#     sessionID = request.data.get('session_id')

#     try:
#         audioObjs = AudioRecordings.objects.filter(session_id_id = sessionID)
#         with zipfile.ZipFile('audioRecordings.zip', 'w') as myZipFile:
#             for audio in audioObjs:
#                 myZipFile.write(audio.audio_path.path, os.path.basename(audio.audio_path.path))
        
#         print('here')
#         return FileResponse(open('audioRecordings.zip', 'rb'), as_attachment=True, status=200)
#         #return Response(status=200)
#     except:
#         print("error")
#         return Response(status=500)



@api_view(['POST'])
def transcribe(request):
    user = request.user.id
    session_id = request.data['session_id']
    blob = request.FILES['audio'] 
    tempAudioFile = 'chunk_audio.wav'

    # write audio blob into a audio file
    with open(tempAudioFile, 'wb+') as destination:
        for chunk in blob.chunks():
            destination.write(chunk)
    
    # whisper transcription process
    print("transcribing")
    result = model.transcribe(tempAudioFile, condition_on_previous_text=False, word_timestamps=True, hallucination_silence_threshold=4, fp16=False, language="en")

    print("Whisper:",result["text"])

    try:
        session = Sessions.objects.get(id=session_id, user_id_id=user)
        if session.transcription is None:
            session.transcription = result["text"]
        else:
            session.transcription += result["text"]
        
        session.save()
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    text = result["text"]
    return Response({'transcription':text}, status=status.HTTP_200_OK)
        
