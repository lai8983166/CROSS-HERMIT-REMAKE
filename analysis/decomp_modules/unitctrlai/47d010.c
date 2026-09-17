
void FUN__text__0047d010(int param_1)

{
  char cVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_60 [16];
  int local_20;
  ushort local_1c;
  ushort local_18;
  short local_14;
  short local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_60;
  for (iVar2 = 0x17; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = FUN__text__0047a8e0(param_1);
  local_10 = (short)((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                          (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
  local_14 = (short)((int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                          (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
  local_18 = (ushort)*(byte *)(local_c + 0x3c);
  local_1c = (ushort)*(byte *)(local_c + 0x3d);
  cVar1 = FUN__text__004ddbb0(param_1);
  local_20 = (int)cVar1;
  FUN__text__0043c1d0((int)local_10,(int)local_14,(int)(short)local_18,(int)(short)local_1c,local_20
                     );
  local_8 = 0x47d0d8;
  FUN__text__0056ce80();
  return;
}

