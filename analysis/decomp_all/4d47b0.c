
void FUN__text__004d47b0(short param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined4 local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((DAT_007a4a00 != 0) && (DAT_007a49fc != 0)) {
    local_c = FUN__text__00450170((&PTR_s_data_sound_voice_v901_v901_001_0_00624adc)[param_1]);
    FUN__text__0041e190(local_c,0);
    FUN__text__0042b2d0(&DAT_005c81fc,(int)param_1,local_c);
  }
  local_8 = 0x4d4837;
  FUN__text__0056ce80();
  return;
}

