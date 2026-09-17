
void FUN__text__00440fe0(short param_1,short param_2,undefined4 param_3)

{
  short sVar1;
  short sVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_54 [16];
  undefined4 local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_54;
  for (iVar3 = 0x14; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_c = (int)param_1;
  sVar1 = __ftol();
  local_10 = (int)param_2;
  sVar2 = __ftol();
  sVar1 = sVar1 + *(short *)(local_8 + 0x2646c);
  sVar2 = sVar2 + *(short *)(local_8 + 0x26470);
  local_14 = param_3;
  switch(param_3) {
  case 0:
    FUN__text__00410310(sVar1 + -1,sVar2 + -1,3,3,0xc6,0xff00ffff,0);
    break;
  case 1:
    FUN__text__00410310(sVar1 + -1,sVar2 + -1,3,3,0xc6,0xff00ff00,0);
    break;
  case 2:
    FUN__text__00410310(sVar1 + -1,sVar2 + -1,3,3,0xc6,0xffc8c83c,0);
    break;
  case 3:
    FUN__text__00410310(sVar1 + -1,sVar2 + -1,3,3,0xc6,0xffff00ff,0);
  }
  local_8 = 0x44114d;
  FUN__text__0056ce80();
  return;
}

