
void FUN__text__004b8790(undefined2 param_1,undefined2 param_2,uint param_3,char param_4,
                        undefined2 param_5)

{
  uint uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  char local_14;
  uint local_10;
  undefined *local_c;
  undefined4 local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = &DAT_0061bf00;
  uVar1 = local_10 >> 0x10;
  local_10 = local_10 & 0xffff0000;
  local_14 = param_4;
  if (param_4 == '\x02') {
    local_10 = CONCAT22((short)uVar1,DAT_0061bf0a);
  }
  iVar2 = (param_3 & 0xffff) * (uint)DAT_0061bf0a * 2 + (local_10 & 0xffff);
  FUN__text__004d2790(&DAT_0061bf00,1,param_5,CONCAT22((short)((uint)iVar2 >> 0x10),param_1),
                      CONCAT22((short)((uint)DAT_0061bf0a * 2 >> 0x10),param_2),0,iVar2);
  local_8 = 0x4b8828;
  FUN__text__0056ce80();
  return;
}

