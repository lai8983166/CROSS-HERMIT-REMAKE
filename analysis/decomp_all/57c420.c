
byte * FUN__text__0057c420(byte *param_1,byte *param_2,size_t param_3)

{
  byte bVar1;
  byte *pbVar2;
  byte *pbVar3;
  size_t sVar4;
  byte *pbVar5;
  
  pbVar3 = param_1;
  if (DAT_0080a91c == 0) {
    pbVar3 = (byte *)_strncpy((char *)param_1,(char *)param_2,param_3);
  }
  else {
    FUN__text__00577040(0x19);
    pbVar2 = param_1;
    do {
      while( true ) {
        param_1 = pbVar2;
        if (param_3 == 0) goto LAB__text__0057c513;
        sVar4 = param_3 - 1;
        if (((&DAT_0080aa21)[*param_2] & 4) == 0) break;
        *param_1 = *param_2;
        pbVar5 = param_1 + 1;
        if (sVar4 == 0) {
          *param_1 = 0;
          param_1 = pbVar5;
          param_3 = sVar4;
          goto LAB__text__0057c513;
        }
        param_3 = param_3 - 2;
        *pbVar5 = param_2[1];
        param_2 = param_2 + 2;
        pbVar2 = param_1 + 2;
        if (*pbVar5 == 0) {
          *param_1 = 0;
          param_1 = param_1 + 2;
          goto LAB__text__0057c513;
        }
      }
      *param_1 = *param_2;
      bVar1 = *param_1;
      param_1 = param_1 + 1;
      param_2 = param_2 + 1;
      pbVar2 = param_1;
      param_3 = sVar4;
    } while (bVar1 != 0);
LAB__text__0057c513:
    while (param_3 != 0) {
      *param_1 = 0;
      param_1 = param_1 + 1;
      param_3 = param_3 - 1;
    }
    FUN__text__005770e0(0x19);
  }
  return pbVar3;
}

