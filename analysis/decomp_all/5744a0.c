
void FUN__text__005744a0(undefined4 *param_1,int param_2,int param_3,undefined4 param_4)

{
  char *pcVar1;
  int iVar2;
  int *piVar3;
  undefined1 uVar4;
  undefined1 local_30 [24];
  int local_18 [4];
  char *local_8;
  
  uVar4 = 0;
  piVar3 = local_18;
  FUN__text__005853b0(*param_1,param_1[1],local_18,local_30);
  iVar2 = piVar3[1] + -1;
  local_8 = (char *)(param_2 + (uint)(*piVar3 == 0x2d));
  FUN__text__005852b0(local_8,param_3,piVar3,piVar3,iVar2,uVar4);
  if ((piVar3[1] + -1 < -4) || (param_3 <= piVar3[1] + -1)) {
    FUN__text__00574180(param_2,param_3,param_4,piVar3,1);
  }
  else {
    pcVar1 = local_8;
    if (iVar2 < piVar3[1] + -1) {
      do {
        local_8 = pcVar1;
        pcVar1 = local_8 + 1;
      } while (*local_8 != '\0');
      local_8[-1] = '\0';
      local_8 = local_8 + 1;
    }
    FUN__text__00574360(param_2,param_3,piVar3,1);
  }
  return;
}

