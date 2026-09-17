
void __thiscall FUN__text__004d5d10(undefined2 *param_1,undefined4 *param_2)

{
  ushort uVar1;
  char cVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_64 [16];
  undefined2 local_24;
  undefined2 local_20;
  undefined2 local_1c;
  undefined2 local_18;
  char local_14;
  undefined3 uStack_13;
  ushort local_10;
  undefined2 uStack_e;
  uint local_c;
  undefined2 *local_8;
  
  puVar4 = local_64;
  for (iVar3 = 0x18; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  *param_2 = 0;
  param_2[1] = 0;
  param_2[2] = 0;
  *(undefined2 *)(param_2 + 3) = 0;
  local_18 = *(undefined2 *)(DAT_007a49fc + 0x196c);
  local_1c = *(undefined2 *)(DAT_007a49fc + 0x1970);
  local_20 = 2;
  local_24 = 2;
  local_c = local_c & 0xffff0000;
  local_8 = param_1;
  while ((local_c & 0xffff) < (uint)(ushort)local_8[2]) {
    uVar1 = local_8[(local_c & 0xffff) + 3];
    _local_10 = CONCAT22(uStack_e,uVar1);
    cVar2 = FUN__text__004d5a60(local_18,local_1c,local_20,local_24,
                                *(undefined2 *)(&DAT_006253c8 + (uint)uVar1 * 8),
                                *(undefined2 *)(&DAT_006253ca + (uint)uVar1 * 8),
                                *(undefined2 *)(&DAT_006253cc + (uint)uVar1 * 8),
                                *(undefined2 *)(&DAT_006253ce + (uint)uVar1 * 8),*local_8,local_8[1]
                               );
    _local_14 = CONCAT31(uStack_13,cVar2);
    if (cVar2 == '\x01') {
      *param_2 = *(undefined4 *)(DAT_007a49fc + 0x198c);
      param_2[1] = *(undefined4 *)(DAT_007a49fc + 0x1990);
      param_2[2] = *(undefined4 *)(DAT_007a49fc + 0x19a0);
      *(undefined2 *)(param_2 + 3) = 1;
    }
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  local_8[2] = 0;
  *local_8 = 0;
  local_8[1] = 0;
  local_8 = (undefined2 *)0x4d5eab;
  FUN__text__0056ce80();
  return;
}

