"""Prepare the bounded CloudFormation template. Does not call AWS."""
from pathlib import Path
import json
r=Path(__file__).resolve().parent
sub=lambda s:{'Fn::Sub':s}
ref=lambda s:{'Ref':s}
att=lambda s,a:{'Fn::GetAtt':[s,a]}
resources={
 'EmailKey':{'Type':'AWS::KMS::Key','DeletionPolicy':'Retain','UpdateReplacePolicy':'Retain','Properties':{
  'Description':'Ioleia public early-access email encryption only; separate from God Agent processing',
  'EnableKeyRotation':True,'KeyPolicy':{'Version':'2012-10-17','Statement':[{
   'Sid':'AccountAdministration','Effect':'Allow','Principal':{'AWS':sub('arn:${AWS::Partition}:iam::${AWS::AccountId}:root')},'Action':'kms:*','Resource':'*'}]}}},
 'EmailKeyAlias':{'Type':'AWS::KMS::Alias','Properties':{'AliasName':'alias/ioleia-website-early-access','TargetKeyId':ref('EmailKey')}},
 'Contacts':{'Type':'AWS::DynamoDB::Table','DeletionPolicy':'Retain','UpdateReplacePolicy':'Retain','Properties':{
  'TableName':'ioleia-website-early-access','BillingMode':'PAY_PER_REQUEST','DeletionProtectionEnabled':True,
  'AttributeDefinitions':[{'AttributeName':'email_key','AttributeType':'S'}],
  'KeySchema':[{'AttributeName':'email_key','KeyType':'HASH'}],
  'SSESpecification':{'SSEEnabled':True,'SSEType':'KMS'},
  'Tags':[{'Key':'Purpose','Value':'PublicWebsiteEarlyAccess'},{'Key':'RealDataAdmission','Value':'false'}]}},
 'SignupLogs':{'Type':'AWS::Logs::LogGroup','Properties':{'LogGroupName':'/aws/lambda/ioleia-website-early-access','RetentionInDays':7}},
 'SignupRole':{'Type':'AWS::IAM::Role','Properties':{
  'RoleName':'ioleia-website-early-access','AssumeRolePolicyDocument':{'Version':'2012-10-17','Statement':[{'Effect':'Allow','Principal':{'Service':'lambda.amazonaws.com'},'Action':'sts:AssumeRole'}]},
  'Policies':[{'PolicyName':'InsertEncryptedWebsiteSignupOnly','PolicyDocument':{'Version':'2012-10-17','Statement':[
   {'Effect':'Allow','Action':'dynamodb:PutItem','Resource':att('Contacts','Arn')},
   {'Effect':'Allow','Action':'kms:Encrypt','Resource':att('EmailKey','Arn'),'Condition':{'StringEquals':{'kms:EncryptionContext:purpose':'ioleia-early-access-email'}}},
   {'Effect':'Allow','Action':['logs:CreateLogStream','logs:PutLogEvents'],'Resource':sub('arn:${AWS::Partition}:logs:${AWS::Region}:${AWS::AccountId}:log-group:/aws/lambda/ioleia-website-early-access:*')}
  ]}}]}},
 'SignupFunction':{'Type':'AWS::Lambda::Function','DependsOn':'SignupLogs','Properties':{
  'FunctionName':'ioleia-website-early-access','Runtime':'python3.13','Handler':'index.lambda_handler','MemorySize':128,'Timeout':10,
  'Role':att('SignupRole','Arn'),'Environment':{'Variables':{'CONTACTS_TABLE':ref('Contacts'),'EMAIL_KEY_ID':att('EmailKey','Arn')}},
  'Code':{'ZipFile':(r/'handler.py').read_text()},
  'Tags':[{'Key':'Purpose','Value':'PublicWebsiteEarlyAccess'}]}},
 'SignupApi':{'Type':'AWS::ApiGatewayV2::Api','Properties':{'Name':'ioleia-website-early-access','ProtocolType':'HTTP',
  'CorsConfiguration':{'AllowOrigins':['https://ioleia.com'],'AllowMethods':['POST'],'AllowHeaders':['content-type'],'AllowCredentials':False,'MaxAge':300}}},
 'SignupIntegration':{'Type':'AWS::ApiGatewayV2::Integration','Properties':{'ApiId':ref('SignupApi'),'IntegrationType':'AWS_PROXY',
  'IntegrationUri':att('SignupFunction','Arn'),'PayloadFormatVersion':'2.0','TimeoutInMillis':12000}},
 'SignupRoute':{'Type':'AWS::ApiGatewayV2::Route','Properties':{'ApiId':ref('SignupApi'),'RouteKey':'POST /early-access','AuthorizationType':'NONE',
  'Target':{'Fn::Join':['/', ['integrations',ref('SignupIntegration')]]}}},
 'SignupStage':{'Type':'AWS::ApiGatewayV2::Stage','Properties':{'ApiId':ref('SignupApi'),'StageName':'$default','AutoDeploy':True,
  'DefaultRouteSettings':{'ThrottlingBurstLimit':5,'ThrottlingRateLimit':1,'DetailedMetricsEnabled':False}}},
 'SignupPermission':{'Type':'AWS::Lambda::Permission','Properties':{'FunctionName':ref('SignupFunction'),'Action':'lambda:InvokeFunction',
  'Principal':'apigateway.amazonaws.com','SourceAccount':ref('AWS::AccountId'),'SourceArn':sub('arn:${AWS::Partition}:execute-api:${AWS::Region}:${AWS::AccountId}:${SignupApi}/*/POST/early-access')}}
}
t={'AWSTemplateFormatVersion':'2010-09-09','Description':'Bounded Ioleia public website intake. No auth, inference, SES, DNS or core Alpha changes.',
   'Resources':resources,'Outputs':{'SignupEndpoint':{'Value':sub('https://${SignupApi}.execute-api.${AWS::Region}.${AWS::URLSuffix}/early-access')},
   'ContactsTable':{'Value':ref('Contacts')},'EmailKeyArn':{'Value':att('EmailKey','Arn')},'FunctionName':{'Value':ref('SignupFunction')}}}
(r/'template.json').write_text(json.dumps(t,indent=2)+'\n')
print('Prepared',len(resources),'resources; no AWS calls made.')
