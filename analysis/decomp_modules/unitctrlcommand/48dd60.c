
void FUN__text__0048dd60(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  undefined4 *local_18;
  undefined4 *local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = FUN__text__00427d60();
  if ((local_c == 0) &&
     (iVar2 = FUN__text__00424f80("ucom!=0",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCommand.cpp",
                                  DAT_00618f9c + 0xb,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_14 = *(undefined4 **)(param_2 + 8);
  local_18 = *(undefined4 **)(local_c + 8);
  *local_18 = *local_14;
  local_18[1] = local_14[1];
  local_18[2] = local_14[2];
  local_18[3] = local_14[3];
  if (*(int *)(param_1 + 0x518) == 0) {
    FUN__text__00427990(param_1 + 0x514,local_c);
  }
  else {
    for (local_10 = *(int *)(param_1 + 0x518); *(int *)(local_10 + 4) != 0;
        local_10 = *(int *)(local_10 + 4)) {
    }
    FUN__text__00427990(local_10,local_c);
  }
  local_8 = 0x48de4c;
  FUN__text__0056ce80();
  return;
}

