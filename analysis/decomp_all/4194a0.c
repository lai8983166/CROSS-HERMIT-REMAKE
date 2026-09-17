
void __fastcall FUN__text__004194a0(int param_1)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_48 [16];
  int local_8;
  
  puVar4 = local_48;
  for (iVar3 = 0x11; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_8 = param_1;
  if ((*(int *)(param_1 + 0x134) != 0) &&
     (iVar3 = FUN__text__00424f80("hEvent==0",
                                  "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                  DAT_005ff560 + 2,0), iVar3 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (*(int *)(local_8 + 0x134) == 0) {
    (*API_KERNEL32_DLL_CreateEventA)(0,0,0,0);
    uVar2 = FUN__text__0056ce80();
    *(undefined4 *)(local_8 + 0x134) = uVar2;
  }
  local_8 = 0x41953b;
  FUN__text__0056ce80();
  return;
}

