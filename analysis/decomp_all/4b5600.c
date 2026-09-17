
/* WARNING: Removing unreachable block (ram,0x004b5945) */

void __fastcall FUN__text__004b5600(int param_1)

{
  ushort uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  ushort local_18;
  undefined2 uStack_16;
  short local_14;
  short local_10;
  short local_c;
  int local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  DAT_007d6a34 = 0;
  local_8 = param_1;
  FUN__text__004d6090(*(undefined4 *)(param_1 + 0xc8c),6);
  FUN__text__004d6090(*(undefined4 *)(local_8 + 0xc8c),10);
  FUN__text__004d6090(*(undefined4 *)(local_8 + 0xc8c),1);
  FUN__text__004d6090(*(undefined4 *)(local_8 + 0xc8c),1);
  FUN__text__004d6090(*(undefined4 *)(local_8 + 0xc8c),1);
  FUN__text__004d6090(*(undefined4 *)(local_8 + 0xc8c),1);
  FUN__text__004d6090(*(undefined4 *)(local_8 + 0xc8c),1);
  FUN__text__004d6090(*(undefined4 *)(local_8 + 0xc8c),4);
  FUN__text__004d6090(*(undefined4 *)(local_8 + 0xc8c),4);
  FUN__text__004d6420("data/YsText/KSCapabilityUP.ybc");
  FUN__text__004d6420("data/YsText/ItemExp.ybc");
  FUN__text__004d6420("data/YsText/SkillExp.ybc");
  FUN__text__004d6420("data/YsText/JobExp.ybc");
  FUN__text__00464d30();
  FUN__text__004b55a0(local_8 + 0x3a1a0,"data/AllResult/AnmAllResult.bin",0x11);
  for (local_c = 0; local_c < 10; local_c = local_c + 1) {
    FUN__text__00409ef0(local_8 + 0x3a1f4 + local_c * 0x58);
  }
  FUN__text__004077c0(DAT_007a49fc);
  local_14 = 0;
  for (local_c = 0; local_c < 0x32; local_c = local_c + 1) {
    *(undefined2 *)(local_8 + 0x596 + local_c * 2) = 0xffff;
    *(undefined1 *)(local_8 + 0x5fa + (int)local_c) = 0xff;
  }
  for (local_c = 0; local_c < 5; local_c = local_c + 1) {
    if (*(short *)(&DAT_007aaa12 + local_c * 0x1c) != -1) {
      for (local_10 = 0; local_10 < 4; local_10 = local_10 + 1) {
        if (*(short *)(&DAT_007aaa22 + local_10 * 2 + local_c * 0x1c) != -1) {
          *(ushort *)(local_8 + 0x596 + local_14 * 2) =
               (ushort)(byte)(&DAT_007aaa22)[local_10 * 2 + local_c * 0x1c];
          *(undefined1 *)(local_8 + 0x5fa + (int)local_14) = (undefined1)local_c;
          local_14 = local_14 + 1;
        }
      }
    }
  }
  for (local_c = 0; local_c < DAT_007d57de; local_c = local_c + 1) {
    if (*(short *)(&DAT_007d57e2 + local_c * 2) != -1) {
      *(undefined2 *)(local_8 + 0x596 + local_14 * 2) = *(undefined2 *)(&DAT_007d57e2 + local_c * 2)
      ;
      local_14 = local_14 + 1;
    }
  }
  *(short *)(local_8 + 0x594) = local_14;
  for (local_c = 0; local_c < *(short *)(local_8 + 0x594); local_c = local_c + 1) {
    if (*(short *)(local_8 + 0x596 + local_c * 2) == DAT_007d57c2) {
      DAT_007d6a34 = local_c;
    }
  }
  uVar1 = *(ushort *)(local_8 + 0x596 + DAT_007d6a34 * 2);
  _local_18 = CONCAT22(uStack_16,uVar1);
  *(undefined2 *)(local_8 + 0x632) = *(undefined2 *)(&DAT_007e17ee + (uint)uVar1 * 0x4a0);
  FUN__text__004b6690(CONCAT22((short)((uint)uVar1 * 0x4a0 >> 0x10),uVar1),0xffffffff,1,2);
  local_8 = 0x4b59f6;
  FUN__text__0056ce80();
  return;
}

