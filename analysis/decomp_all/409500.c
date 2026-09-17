
void __thiscall FUN__text__00409500(int param_1,char *param_2)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  undefined4 local_58 [16];
  undefined4 local_18;
  undefined4 local_14;
  undefined4 local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_58;
  for (iVar3 = 0x15; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_8 = param_1;
  if ((*(int *)(param_1 + 0x4c) == 0) &&
     (iVar3 = FUN__text__00424f80("DxSys",
                                  "E:\\CrossHermit\\GAME\\SRC\\SYSTEM\\DIRECTX\\D3dxSpFont.cpp",
                                  DAT_005ff0bc + 3,0), iVar3 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((*(int *)(local_8 + 0x84) == 0) &&
     (iVar3 = FUN__text__00424f80("hFont",
                                  "E:\\CrossHermit\\GAME\\SRC\\SYSTEM\\DIRECTX\\D3dxSpFont.cpp",
                                  DAT_005ff0bc + 4,0), iVar3 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((*(int *)(local_8 + 0x4c) != 0) && (*(int *)(local_8 + 0x84) != 0)) {
    if (*(int *)(local_8 + 0x80) != 0) {
      iVar3 = _strcmp(param_2,*(char **)(local_8 + 0x80));
      if (iVar3 == 0) goto LAB__text__004096bd;
      if (*(int *)(local_8 + 0x80) != 0) {
        local_14 = *(undefined4 *)(local_8 + 0x80);
        FUN__text__00428ad0(local_14);
      }
    }
    (*API_KERNEL32_DLL_lstrlenA)(param_2);
    local_c = FUN__text__0056ce80();
    local_c = local_c + 1;
    local_18 = FUN__text__00428a40(local_c);
    *(undefined4 *)(local_8 + 0x80) = local_18;
    if ((*(int *)(local_8 + 0x80) == 0) &&
       (iVar3 = FUN__text__00424f80("str_cache",
                                    "E:\\CrossHermit\\GAME\\SRC\\SYSTEM\\DIRECTX\\D3dxSpFont.cpp",
                                    DAT_005ff0bc + 0x11,0), iVar3 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    (*API_KERNEL32_DLL_lstrcpyA)(*(undefined4 *)(local_8 + 0x80),param_2);
    FUN__text__0056ce80();
    iVar3 = (int)*(char *)(local_8 + 0x88);
    uVar6 = *(undefined4 *)(local_8 + 0x80);
    uVar5 = *(undefined4 *)(local_8 + 0x84);
    uVar2 = FUN__text__004142b0(uVar5,uVar6,iVar3);
    local_10 = FUN__text__00408e30(uVar2,uVar5,uVar6,iVar3);
  }
LAB__text__004096bd:
  local_8 = 0x4096ca;
  FUN__text__0056ce80();
  return;
}

