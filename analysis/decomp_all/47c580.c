
void FUN__text__0047c580(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  undefined1 local_14;
  undefined1 local_10;
  short local_c;
  undefined4 local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__0047c690(param_1,param_2);
  if (iVar2 == 0) {
    local_c = *(short *)(&DAT_006b2da0 + (uint)*(ushort *)(*(int *)(param_1 + 600) + 0xc) * 0x40);
    if ((local_c == 0) &&
       (iVar2 = FUN__text__00424f80("skill != 0",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                    DAT_00618e58 + 0xb,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_10 = (undefined1)
               ((int)((*(int *)(param_2 + 0x2ec) >> 0x10) +
                     (*(int *)(param_2 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
    local_14 = (undefined1)
               ((int)((*(int *)(param_2 + 0x2f0) >> 0x10) +
                     (*(int *)(param_2 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
    *(undefined2 *)(param_1 + 0x4ee) = *(undefined2 *)(param_2 + 2);
    *(short *)(param_1 + 0x4f2) = local_c;
    *(undefined1 *)(param_1 + 0x4f0) = local_10;
    *(undefined1 *)(param_1 + 0x4f1) = local_14;
  }
  local_8 = 0x47c67d;
  FUN__text__0056ce80();
  return;
}

