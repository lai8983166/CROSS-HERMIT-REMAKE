
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__004a9d90(ushort param_1)

{
  byte bVar1;
  char cVar2;
  byte bVar3;
  short sVar4;
  int iVar5;
  undefined4 *puVar6;
  undefined4 local_68 [18];
  short local_20;
  undefined1 local_1c;
  ushort local_14;
  undefined1 local_c;
  
  sVar4 = DAT_007a5b62;
  puVar6 = local_68;
  for (iVar5 = 0x19; iVar5 != 0; iVar5 = iVar5 + -1) {
    *puVar6 = 0xcccccccc;
    puVar6 = puVar6 + 1;
  }
  bVar1 = (&DAT_0073bed6)[(uint)param_1 * 0x100];
  cVar2 = (&DAT_0073bed7)[(uint)param_1 * 0x100];
  local_14 = (ushort)(byte)(&DAT_0073bed5)[(uint)param_1 * 0x100];
  bVar3 = (&DAT_0073bed4)[(uint)param_1 * 0x100];
  if (local_14 == 99) {
    local_14 = 0xffff;
  }
  if ((ushort)(bVar1 - 1) == 3) {
    local_1c = 0;
  }
  else if (local_14 == 0xffff) {
    local_1c = 1;
  }
  else {
    local_1c = 2;
  }
  DAT_007a5b62 = DAT_007a5b62 + 1;
  for (local_20 = 0; local_20 < sVar4; local_20 = local_20 + 1) {
    *(undefined2 *)(&DAT_007a5662 + ((int)sVar4 - (int)local_20) * 0x10) =
         *(undefined2 *)(&DAT_007a5662 + (((int)sVar4 - (int)local_20) + -1) * 0x10);
    (&DAT_007a5665)[((int)sVar4 - (int)local_20) * 0x10] =
         (&DAT_007a5665)[(((int)sVar4 - (int)local_20) + -1) * 0x10];
    (&DAT_007a5666)[((int)sVar4 - (int)local_20) * 0x10] =
         (&DAT_007a5666)[(((int)sVar4 - (int)local_20) + -1) * 0x10];
    (&DAT_007a5668)[((int)sVar4 - (int)local_20) * 0x10] =
         (&DAT_007a5668)[(((int)sVar4 - (int)local_20) + -1) * 0x10];
    (&DAT_007a5667)[((int)sVar4 - (int)local_20) * 0x10] =
         (&DAT_007a5667)[(((int)sVar4 - (int)local_20) + -1) * 0x10];
    *(undefined2 *)(&DAT_007a566a + ((int)sVar4 - (int)local_20) * 0x10) =
         *(undefined2 *)(&DAT_007a566a + (((int)sVar4 - (int)local_20) + -1) * 0x10);
    *(undefined2 *)(&DAT_007a566c + ((int)sVar4 - (int)local_20) * 0x10) =
         *(undefined2 *)(&DAT_007a566c + (((int)sVar4 - (int)local_20) + -1) * 0x10);
    *(undefined2 *)(&DAT_007a566e + ((int)sVar4 - (int)local_20) * 0x10) =
         *(undefined2 *)(&DAT_007a566e + (((int)sVar4 - (int)local_20) + -1) * 0x10);
    *(undefined2 *)(&DAT_007a5670 + ((int)sVar4 - (int)local_20) * 0x10) =
         *(undefined2 *)(&DAT_007a5670 + (((int)sVar4 - (int)local_20) + -1) * 0x10);
  }
  DAT_007a5664 = 1;
  _DAT_007a5662 = param_1;
  local_c = (undefined1)(bVar1 - 1);
  DAT_007a5665 = local_c;
  DAT_007a5666 = cVar2 + -1;
  DAT_007a5668 = 0;
  DAT_007a5667 = local_1c;
  _DAT_007a566a = local_14;
  _DAT_007a566c = (ushort)bVar3;
  _DAT_007a566e = 0;
  _DAT_007a5670 = 0;
  return;
}

