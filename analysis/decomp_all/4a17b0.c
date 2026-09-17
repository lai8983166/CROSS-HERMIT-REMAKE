
/* WARNING: Removing unreachable block (ram,0x004a1818) */

void __fastcall FUN__text__004a17b0(undefined4 param_1)

{
  uint uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  undefined4 local_14;
  undefined2 local_10;
  undefined2 uStack_e;
  uint local_c;
  undefined4 local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = CONCAT22(local_c._2_2_,1);
  local_8 = param_1;
  while ((local_c & 0xffff) < 0x65) {
    if ((&DAT_007a55fc)[local_c & 0xffff] == '\0') {
      _local_10 = CONCAT22(uStack_e,1);
      if ((((&DAT_0073bed1)[(local_c & 0xffff) * 0x100] != '\0') &&
          ((byte)(&DAT_0073bed2)[(local_c & 0xffff) * 0x100] == DAT_007a528e)) &&
         ((byte)(&DAT_0073bed3)[(local_c & 0xffff) * 0x100] == DAT_007a5290)) {
        uVar1 = local_14 >> 0x10;
        local_14 = local_14 & 0xffff0000;
        if ((&DAT_0073bede)[(local_c & 0xffff) * 0x100] == '\0') {
          local_14 = CONCAT22((short)uVar1,1);
        }
        iVar2 = (local_c & 0xffff) * 0x100;
        if ((&DAT_0073bed6)[iVar2] == '\0') {
          local_14 = CONCAT22(local_14._2_2_,1);
        }
        if ((local_14 & 0xffff) == 0) {
          FUN__text__004a9d90(CONCAT22((short)((uint)iVar2 >> 0x10),(short)local_c));
          (&DAT_007a55fc)[local_c & 0xffff] = 1;
        }
      }
    }
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  local_8 = 0x4a191a;
  FUN__text__0056ce80();
  return;
}

