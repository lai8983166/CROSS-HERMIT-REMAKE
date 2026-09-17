
void FUN__text__0044e7a0(undefined4 param_1,undefined2 param_2,undefined2 param_3,ushort *param_4,
                        ushort *param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  byte *local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = (byte *)FUN__text__0044e740(param_1,param_2,CONCAT22(0xcccc,param_3));
  *param_4 = (ushort)*local_c;
  *param_5 = (ushort)local_c[1];
  local_8 = 0x44e7fe;
  FUN__text__0056ce80();
  return;
}

