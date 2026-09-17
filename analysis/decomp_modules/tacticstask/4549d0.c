
void __thiscall
FUN__text__004549d0(int param_1,undefined4 param_2,undefined4 param_3,int param_4,undefined4 param_5
                   ,undefined4 param_6,int param_7,int param_8)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  if (param_7 == 1) {
    local_c = FUN__text__00455060(param_3,param_4);
    local_10 = FUN__text__00455060(param_3,param_4 + 1);
    local_14 = local_10 - local_c;
    FUN__text__004ce460(local_c,0xffffffff,local_14);
  }
  *(undefined1 *)(local_8 + 0x43) = 1;
  if (param_8 == 1) {
    FUN__text__00467850(1,0);
  }
  _memset((void *)(local_8 + 0x44),0,0x1c);
  *(int *)(local_8 + 0x48) = param_7;
  *(undefined4 *)(local_8 + 0x4c) = param_5;
  *(undefined4 *)(local_8 + 0x50) = param_6;
  *(undefined1 *)(local_8 + 0x59) = 1;
  *(undefined1 *)(local_8 + 0x58) = 0;
  *(int *)(local_8 + 0x54) = param_8;
  local_8 = 0x454aaa;
  FUN__text__0056ce80();
  return;
}

