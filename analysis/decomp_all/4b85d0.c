
void FUN__text__004b85d0(undefined2 param_1,undefined2 param_2,uint param_3,undefined2 param_4)

{
  uint uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  undefined1 local_10;
  byte local_c;
  undefined4 local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = (param_3 & 0xffff) - 1;
  local_c = (byte)(iVar2 / 2);
  uVar1 = (param_3 & 0xffff) - 1 & 0x80000001;
  if ((int)uVar1 < 0) {
    uVar1 = (uVar1 - 1 | 0xfffffffe) + 1;
  }
  local_10 = (undefined1)(uVar1 + 1);
  FUN__text__004b8660(CONCAT22((short)(iVar2 >> 0x1f),param_1),param_2,
                      CONCAT22((short)(uVar1 + 1 >> 0x10),(ushort)local_c),
                      CONCAT31((int3)(iVar2 >> 0x1f),local_10),param_4);
  local_8 = 0x4b864b;
  FUN__text__0056ce80();
  return;
}

