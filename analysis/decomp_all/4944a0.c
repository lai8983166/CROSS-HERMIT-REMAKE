
void __thiscall FUN__text__004944a0(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  uint local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_18 = (uint)*(byte *)(*(int *)(param_2 + 600) + 0x98);
  local_8 = param_1;
  if ((10 < local_18) &&
     (iVar2 = FUN__text__00424f80("(0<=group) && (group<=10)",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlKeySelect.cpp",
                                  DAT_006192a0 + 7,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_c = local_8 + 0x116098 + (uint)*(byte *)(*(int *)(param_2 + 600) + 0x98) * 0x2c;
  FUN__text__00427b70(local_c + 0x10);
  do {
    local_10 = FUN__text__00427bf0();
    if (local_10 == 0) break;
    local_14 = *(int *)(local_10 + 8);
    if ((local_14 == 0) &&
       (iVar2 = FUN__text__00424f80("uwk!=0",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlKeySelect.cpp",
                                    DAT_006192a0 + 0xf,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  } while (local_14 != param_2);
  local_8 = 0x4945a6;
  FUN__text__0056ce80();
  return;
}

