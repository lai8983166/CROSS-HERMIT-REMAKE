
void FUN__text__0047ce70(int param_1,int param_2)

{
  undefined1 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_64 [16];
  char local_24;
  short local_20;
  short local_1c;
  short local_18;
  short local_14;
  undefined1 local_10;
  undefined3 uStack_f;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_64;
  for (iVar2 = 0x18; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = FUN__text__0047a8e0(param_1);
  local_24 = *(char *)(local_c + 0x1e);
  if (local_24 == '\0') {
    iVar2 = (int)(short)((uint)*(undefined4 *)(param_1 + 0x2ec) >> 0x10);
    local_14 = (short)((int)(iVar2 + (iVar2 >> 0x1f & 0x1fU)) >> 5);
    iVar2 = (int)(short)((uint)*(undefined4 *)(param_1 + 0x2f0) >> 0x10);
    local_18 = (short)((int)(iVar2 + (iVar2 >> 0x1f & 0xfU)) >> 4);
    iVar2 = (int)(short)((uint)*(undefined4 *)(param_2 + 0x2ec) >> 0x10);
    local_1c = (short)((int)(iVar2 + (iVar2 >> 0x1f & 0x1fU)) >> 5);
    iVar2 = (int)(short)((uint)*(undefined4 *)(param_2 + 0x2f0) >> 0x10);
    local_20 = (short)((int)(iVar2 + (iVar2 >> 0x1f & 0xfU)) >> 4);
    uVar1 = FUN__text__004ddbb0(param_1);
    _local_10 = CONCAT31(uStack_f,uVar1);
    iVar2 = FUN__text__0043c1d0((int)local_14,(int)local_18,(int)local_1c,(int)local_20,uVar1);
    if ((iVar2 != 0) && (iVar2 = FUN__text__0047c580(param_1,param_2), iVar2 != 0)) {
      FUN__text__00475270(param_1,6);
      FUN__text__00492e60(param_1 + 0x4fa);
      goto LAB__text__0047cff1;
    }
  }
  else if (local_24 == '\x02') {
    *(undefined2 *)(param_1 + 0x4ee) = *(undefined2 *)(param_2 + 2);
    FUN__text__00475270(param_1,0x1d);
    FUN__text__00492e60(param_1 + 0x4fa);
    goto LAB__text__0047cff1;
  }
  FUN__text__00492e60(param_1 + 0x4fa);
LAB__text__0047cff1:
  local_8 = 0x47cffe;
  FUN__text__0056ce80();
  return;
}

