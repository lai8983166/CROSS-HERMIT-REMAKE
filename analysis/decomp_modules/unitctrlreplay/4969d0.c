
/* WARNING: Removing unreachable block (ram,0x00496add) */

void FUN__text__004969d0(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  undefined4 *local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__00496450();
  if (iVar2 != 0) {
    while ((**(int **)(local_8 + 0x117c44) != 0x7fffffff &&
           (**(int **)(local_8 + 0x117c44) == *(int *)(local_8 + 0x2e6f8)))) {
      local_c = FUN__text__00427d60();
      if ((local_c == 0) &&
         (iVar2 = FUN__text__00424f80("ldst!=0",
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlRePlay.cpp",
                                      DAT_00619f78 + 0x12,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      local_10 = *(undefined4 **)(local_c + 8);
      iVar2 = *(int *)(local_8 + 0x117c44);
      *local_10 = *(undefined4 *)(iVar2 + 0xc);
      local_10[1] = *(undefined4 *)(iVar2 + 0x10);
      local_10[2] = *(undefined4 *)(iVar2 + 0x14);
      local_10[3] = *(undefined4 *)(iVar2 + 0x18);
      FUN__text__00427e30(local_c);
      *(int *)(local_8 + 0x117c44) = *(int *)(local_8 + 0x117c44) + 0x1c;
    }
  }
  local_8 = 0x496aec;
  FUN__text__0056ce80();
  return;
}

