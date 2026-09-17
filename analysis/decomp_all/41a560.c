
void __fastcall FUN__text__0041a560(int *param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  int *local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if ((*param_1 == 0) &&
     (iVar2 = FUN__text__00424f80("pDxPlay!=0",
                                  "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                  DAT_005ff584 + 1,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((local_8[0x4d] == 0) &&
     (iVar2 = FUN__text__00424f80("hEvent!=0",
                                  "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                  DAT_005ff584 + 2,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((local_8[0x4f] != 0) &&
     (iVar2 = FUN__text__00424f80("thParam.hThread==0",
                                  "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                  DAT_005ff584 + 3,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_8[0x57] = local_8[0x5dd];
  local_8[0x58] = *local_8;
  local_8[0x59] = local_8[0x4d];
  local_8[0x5a] = (int)(local_8 + 0x5b);
  iVar2 = FUN__text__0056e050(0,0,FUN__text__0041a800,local_8 + 0x4f,0,local_8 + 0x50);
  local_8[0x4f] = iVar2;
  if ((local_8[0x4f] == 0) &&
     (iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                  DAT_005ff584 + 0x18,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_8 = (int *)0x41a6ca;
  FUN__text__0056ce80();
  return;
}

