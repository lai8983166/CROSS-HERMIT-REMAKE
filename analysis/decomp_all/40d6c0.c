
void __thiscall FUN__text__0040d6c0(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (((*(int *)(param_1 + 8) != 0) && (*(int *)(param_1 + 0xc) != 0)) &&
     (*(int *)(param_1 + 0x10) != 0)) {
    if (2000 < param_2) {
      param_2 = 2000;
    }
    if (param_2 < -20000) {
      param_2 = -20000;
    }
    local_8 = param_1;
    (**(code **)(**(int **)(param_1 + 8) + 0x88))
              (*(undefined4 *)(param_1 + 8),&DAT_005cb08c,&param_2,4);
    local_c = FUN__text__0056ce80();
    if (local_c < 0) {
      FUN__text__0056cbca("E:\\CrossHermit\\GAME\\src\\SYSTEM\\DIRECTX\\DXAudio.CPP",
                          DAT_005ff144 + 0xe,local_c,"SetMasterVolume()",1);
    }
    else {
      *(int *)(local_8 + 4) = param_2;
    }
  }
  local_8 = 0x40d7a7;
  FUN__text__0056ce80();
  return;
}

