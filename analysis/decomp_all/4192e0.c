
void __thiscall FUN__text__004192e0(undefined4 *param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_68 [16];
  int local_28;
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  undefined4 local_14;
  int local_10;
  int local_c;
  undefined4 *local_8;
  
  puVar3 = local_68;
  for (iVar2 = 0x19; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  (**(code **)(*(int *)*param_1 + 0x58))(*param_1,0,&local_14);
  FUN__text__0056ce80();
  local_1c = FUN__text__00428a40(local_14);
  local_18 = local_1c;
  if (local_1c == 0) {
    iVar2 = FUN__text__00424f80("addr != 0",
                                "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                DAT_005ff55c + 10,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  (**(code **)(*(int *)*local_8 + 0x58))(*local_8,local_18,&local_14);
  local_10 = FUN__text__0056ce80();
  if (local_10 == 0) {
    local_c = local_18;
    if (param_2 == 0) {
      *(uint *)(local_18 + 4) = *(uint *)(local_18 + 4) | 0x20;
    }
    else {
      *(uint *)(local_18 + 4) = *(uint *)(local_18 + 4) & 0xffffffdf;
    }
    (**(code **)(*(int *)*local_8 + 0x7c))(*local_8,local_18,0);
    local_10 = FUN__text__0056ce80();
    if (local_10 == 0) {
      local_28 = local_18;
      FUN__text__00428ad0(local_18);
    }
    else {
      local_24 = local_18;
      FUN__text__00428ad0(local_18);
      FUN__text__0041b4a0(local_10);
    }
  }
  else {
    local_20 = local_18;
    FUN__text__00428ad0(local_18);
    FUN__text__0041b4a0(local_10);
  }
  local_20 = 0x419447;
  FUN__text__0056ce80();
  return;
}

