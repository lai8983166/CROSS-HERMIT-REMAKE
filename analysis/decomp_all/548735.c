
int __thiscall FUN__text__00548735(int param_1,int *param_2)

{
  undefined4 *puVar1;
  int iVar2;
  undefined4 uVar3;
  undefined4 *puVar4;
  undefined1 local_e8 [12];
  uint local_dc;
  undefined1 local_14 [16];
  
  *(int *)(param_1 + 0xac) = DAT_0080a398;
  DAT_0080a398 = param_1;
  *(int **)(param_1 + 4) = param_2;
  (**(code **)(*param_2 + 4))(param_2);
  (**(code **)(**(int **)(param_1 + 4) + 0x1c))(*(int **)(param_1 + 4),local_e8);
  (**(code **)(**(int **)(param_1 + 4) + 0x24))(*(int **)(param_1 + 4),local_14);
  *(uint *)(param_1 + 0x50) = local_dc & 0x20000000;
  *(undefined4 *)(param_1 + 0x58) = 0x40;
  *(undefined4 *)(param_1 + 0x5c) = 0x10;
  *(undefined4 *)(param_1 + 0x54) = 0x15;
  iVar2 = FUN__text__0054864c();
  if ((-1 < iVar2) &&
     (iVar2 = FUN__text__0052ae80(*(undefined4 *)(param_1 + 4),param_1 + 0xc), -1 < iVar2)) {
    puVar1 = (undefined4 *)(param_1 + 0x70);
    puVar4 = puVar1;
    for (iVar2 = 10; iVar2 != 0; iVar2 = iVar2 + -1) {
      *puVar4 = 0;
      puVar4 = puVar4 + 1;
    }
    *puVar1 = 0x28;
    *(undefined4 *)(param_1 + 0x74) = 0x100;
    *(undefined4 *)(param_1 + 0x78) = 0x100;
    *(undefined2 *)(param_1 + 0x7c) = 1;
    *(undefined4 *)(param_1 + 0x80) = 0;
    *(undefined2 *)(param_1 + 0x7e) = 0x20;
    *(undefined4 *)(param_1 + 0xa4) = 0x15;
    iVar2 = (*API_GDI32_DLL_CreateCompatibleDC)(0);
    *(int *)(param_1 + 0x6c) = iVar2;
    if (iVar2 != 0) {
      *(int *)(param_1 + 0x78) = -*(int *)(param_1 + 0x78);
      iVar2 = (*API_GDI32_DLL_CreateDIBSection)(iVar2,puVar1,0,param_1 + 0xa0,0,0);
      *(int *)(param_1 + 0x98) = iVar2;
      if (iVar2 != 0) {
        *(int *)(param_1 + 0x78) = -*(int *)(param_1 + 0x78);
        (*API_GDI32_DLL_SetBkMode)(*(undefined4 *)(param_1 + 0x6c),2);
        (*API_GDI32_DLL_SetBkColor)(*(undefined4 *)(param_1 + 0x6c),0);
        (*API_GDI32_DLL_SetTextColor)(*(undefined4 *)(param_1 + 0x6c),0xffffff);
        uVar3 = (*API_GDI32_DLL_SelectObject)
                          (*(undefined4 *)(param_1 + 0x6c),*(undefined4 *)(param_1 + 0x98));
        *(undefined4 *)(param_1 + 0x9c) = uVar3;
        return 0;
      }
    }
    iVar2 = -0x7ff8fff2;
  }
  return iVar2;
}

