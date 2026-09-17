
void __thiscall FUN__text__0049c560(int param_1,short param_2,short param_3)

{
  int iVar1;
  undefined2 uVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if ((((*(int *)(param_1 + 0x108b50) != 0) && (param_2 < 0x18c)) && (599 < param_3)) &&
     (*(short *)(param_1 + 0x109d4e) != -1)) {
    local_8 = param_1;
    for (local_c = 0; local_c != 0x18; local_c = local_c + 1) {
      if (local_c != 0xf) {
        uVar2 = (undefined2)((uint)local_c >> 0x10);
        iVar1 = FUN__text__00470070(CONCAT22(uVar2,*(undefined2 *)(&DAT_0061aea8 + local_c * 8)),
                                    CONCAT22(uVar2,*(undefined2 *)(&DAT_0061aeaa + local_c * 8)),
                                    CONCAT22(uVar2,*(undefined2 *)(&DAT_0061aeac + local_c * 8)),
                                    *(undefined2 *)(&PTR_DAT_0061aeae + local_c * 2),param_2,param_3
                                   );
        if (iVar1 != 0) {
          *(undefined1 *)(local_8 + 0x2f15c) = 0;
          *(undefined1 *)(local_8 + 0x2f15e) = (undefined1)local_c;
          break;
        }
      }
    }
  }
  local_8 = 0x49c660;
  FUN__text__0056ce80();
  return;
}

